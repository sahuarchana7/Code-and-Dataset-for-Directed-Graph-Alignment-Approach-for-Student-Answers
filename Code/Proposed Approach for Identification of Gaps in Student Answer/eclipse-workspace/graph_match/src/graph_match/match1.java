package graph_match;
//package graph_match_modify;
import graph_match.StringMatcher;
import graph_match.match1;
import graph_match.match1.PGArc;
import graph_match.match1.PGNode;
import graph_match.match1.StmtPair;

import java.util.*;
import java.io.*;

import org.w3c.rdf.model.*;

import com.interdataworking.*;
import com.interdataworking.mm.alg.MapPair;

import org.w3c.rdf.util.*;
//import org.javatuples.Triplet;

import static java.util.Arrays.asList;
import static java.util.Collections.emptyList;
import static java.util.Optional.of;
import static java.util.stream.Collectors.toList;

import java.util.List;

public class match1 implements UntypedGateway{
	public boolean DEBUG = false;
	  public static final int DEBUG_MAX_ITERATIONS = 0;

	  // default formula to be used: {ADD_SIGMA0_BEFORE=t, ADD_SIGMA0_AFTER=t, ADD_SIGMAN_AFTER=t}
	  public boolean[] formula = FORMULA_TTT;

	  // default way of computing the propagation coefficients to be used
	  public int FLOW_GRAPH_TYPE = FG_AVG;

	  // various iteration formulas

	  // MAY BE BETTER! but much worse convergence!
	  //   sigma^{n+1} = normalize(f(sigma^0 + sigma^n));
	  public static final boolean[] FORMULA_TFF = {true, false, false};

	  // SLIGHTLY WORSE, BUT BETTER CONVERGENCE!
	  //   sigma^{n+1} = normalize(sigma^0 + sigma^n + f(sigma^0 + sigma^n));
	  public static final boolean[] FORMULA_TTT = {true, true, true};

	  // USE THIS ONE FOR TESTING/DEBUGGING - PURE VERSION
	  //   sigma^{n+1} = normalize(sigma^n + f(sigma^n));
	  public static final boolean[] FORMULA_FFT = {false, false, true};

	  //   sigma^{n+1} = normalize(sigma^0 + f(sigma^n));
	  public static final boolean[] FORMULA_FTF = {false, true, false};

	  //   sigma^{n+1} = normalize(sigma^0 + f(sigma^0 + sigma^n));
	  public static final boolean[] FORMULA_TTF = {true, true, false};

	  //   sigma^{n+1} = normalize(sigma^n + f(sigma^0 + sigma^n));
	  public static final boolean[] FORMULA_TFT = {true, false, true};

	  //   sigma^{n+1} = normalize(sigma^0 + sigma^n + f(sigma^n));
	  public static final boolean[] FORMULA_FTT = {false, true, true};



	  //  static final boolean ADD_SIGMAN_BEFORE = true; // ALWAYS TRUE, OTHERWISE DOES NOT MAKE SENSE
	  static final double MIN_NODE_SIM2 = StringMatcher.MIN_NODE_SIM;

	  // ways of computing propagation coefficients

	  public static final int FG_PRODUCT = 1;
	  public static final int FG_AVG = 2;
	  public static final int FG_EQUAL = 3;
	  public static final int FG_TOTALP = 4;
	  public static final int FG_TOTALS = 5;
	  public static final int FG_AVG_TOTALS = 6;
	  public static final int FG_STOCHASTIC = 7; // weight of OUTGOING normalized to 1
	  public static final int FG_INCOMING = 8; // weight of INCOMING normalized to 1

	  // other variables and constants

	  public static final double UPDATE_GUESS_WEIGHT = 1.0; // between 0 and 1
	  public double RESIDUAL_VECTOR_LENGTH = 0.05; // make this number smaller to increase precision
	  public int MAX_ITERATION_NUM = 10000;
	  //public int MAX_ITERATION_NUM = 1;
	  public int MIN_ITERATION_NUM = 7;
	  //public int MIN_ITERATION_NUM = 1;
	  public int TIMEOUT = 30 * 1000; // 30 sec

	  public boolean TRY_ALL_ARCS = false; // consider all arcs, not only those that are equal
	  public boolean DIRECTED_GRAPH = true;
	  public boolean TEST = true;

	  static final int MIN_CHOICE_ITEMS = 50;
	  public double EQUAL_PRED_COEFF = 1.0;
	  public double OTHER_PRED_COEFF = 0.001;

	  Model m1, m2;

	  Map pgnodes = new HashMap();
	  List pgarcs = new ArrayList();

	  // cache for reusable pairs
	  MapPair[] cachePairs = { new MapPair(), new MapPair() };
	  static final int PASS_PAIR = 0;
	  static final int GET_PAIR = 1;

	  /**
	   * Transforms an ordered list of models into another list of models
	   */
	  public List execute(List input) throws ModelException {

	    Model m1 = (Model)input.get(0);
	    Model m2 = (Model)input.get(1);
	    List sigma0 = null;
	    
	    if(input.size() > 2) {
	      Model initialMap = (Model)input.get(2);
	      sigma0 = MapPair.toMapPairs(initialMap);
	      if(sigma0.size() == 0)
		sigma0 = null;
	    }

	    PGNode[] finalList = getMatch(m1, m2, sigma0);

	    Model map = MapPair.asModel(m1.create(), finalList);
	    ArrayList l = new ArrayList();
	    l.add(map);
	    return l;
	  }

	  public PGNode[] getMatch(Model m1, Model m2, List sigma0) throws ModelException {

	    this.m1 = m1;
	    this.m2 = m2;
	    //    this.sigma0 = rm;

	    // computes sigma0 if null; must go before constructPropagationGraph
	    if(sigma0 == null)
	      initSigma0();
	    else {
	      // set initial values from sigma0
	      for(Iterator it = sigma0.iterator(); it.hasNext();) {

		MapPair p = (MapPair)it.next();
		PGNode n = (PGNode)pgnodes.get(p);
		if(n == null) {
		  n = new PGNode(p.getLeft(), p.getRight());
		  pgnodes.put(n, n);
		}
		n.sim0 = (p.sim == p.NULL_SIM ? 1 : p.sim);
		//System.out.println(pgnodes);
		//System.out.println(n.sim0);
		
		n.inverse = p.inverse; // make sure chosen direction remains unchanged
	      }
	    }

	    // must go AFTER cardMaps
	    boolean ignorePredicates = TRY_ALL_ARCS; // || (FLOW_GRAPH_TYPE == FG_STOCHASTIC);

	    long pgstart = System.currentTimeMillis();
	    System.err.print("Creating propagation graph: ");
	    constructPropagationGraph(ignorePredicates);
	    long pgend = System.currentTimeMillis();
	    System.err.println("" + (double)(pgend - pgstart) / 1000 + " sec");

	    long startTime = System.currentTimeMillis();

	    if(TEST) {
	      //      System.err.println("Pairwise connectivity graph contains " + stmtPairs.size() + " arcs");
	      System.err.println("Propagation graph contains " + pgarcs.size() + " bidirectional arcs and " + pgnodes.size() + " nodes");
	      if(DEBUG) {
//	 	System.err.println("============ Arcs: ==============");
//	 	dump(pgarcs);
//	 	System.err.println("============ Nodes: =============");
//	 	dump(pgnodes.values());
		System.err.println("EQUAL_PRED_COEFF = " + EQUAL_PRED_COEFF + "\n" +
				   "OTHER_PRED_COEFF = " + OTHER_PRED_COEFF + "\n" +
				   "TRY_ALL_ARCS = " + TRY_ALL_ARCS);
	      }
	    }

	    // create arrays for efficiency

	    PGNode[] nodes;
	    PGArc[] arcs;

	    arcs = new PGArc[pgarcs.size()];
	    pgarcs.toArray(arcs);
	    pgarcs = null; // free memory

	    nodes = new PGNode[pgnodes.size()];
	    pgnodes.values().toArray(nodes);
	    pgnodes = null; // free memory

	    if(TEST)
	      System.err.print("Iterating over (" +
			       m1.size() + " arcs, " + RDFUtil.getNodes(m1).size() + " nodes) x (" +
			       m2.size() + " arcs, " + RDFUtil.getNodes(m2).size() + " nodes): ");

	    int iterationNum = MAX_ITERATION_NUM;


	    // initialize sigmaN1 := sigma0;
	    for(int i=0; i < nodes.length; i++) {
	      //      nodes[i].simN1 = rnd.nextDouble();
	      //      nodes[i].sim0 /= 1000;
	      nodes[i].simN1 = nodes[i].sim0;
	    }
	    normalizeN1(nodes);


	    for(int iteration=0; iteration < iterationNum; iteration++) {

	      if(DEBUG && iteration < DEBUG_MAX_ITERATIONS) {
		System.err.println("\nIteration: " + iteration);
		//	debugMap(sigmaN);
	      }
        //System.out.println(arcs);
        //System.out.println(nodes);
        //System.out.println(iteration);
	      applyFormula(arcs, nodes, iteration);
	      
	      System.err.print(".");

	      normalizeN1(nodes);

	      if(DEBUG && iteration < DEBUG_MAX_ITERATIONS) {
		System.err.println("\nAfter norm: " + iteration);
		dump(Arrays.asList(nodes));
	      }

	      double diff = distance(nodes);

//	       double maxN1 = maxN1(nodes);
//	       double diff = distanceF(nodes, maxN, maxN1);
//	       maxN = maxN1;

	      if(TEST) {
		if(DEBUG && iteration < DEBUG_MAX_ITERATIONS)
		  System.err.println("------------------");
		System.err.print("(" + iteration + ":" + diff + ")");
	      }

	      if(iteration >= MIN_ITERATION_NUM && diff <= RESIDUAL_VECTOR_LENGTH)
		break; // we are done!
	      if(System.currentTimeMillis() - startTime > TIMEOUT)
	  	break;

	      // copy sigmaN+1 into sigmaN and repeat: done at top of loop
	    }
	    // RETURN

	    if(TEST)
	      System.err.println(". Time: " +
				 ((double)(System.currentTimeMillis() - startTime) / 1000) + " sec");

	    // copy result into sim
	    for(int i=0; i < nodes.length; i++)
	      nodes[i].sim = nodes[i].simN1; // / maxN;

	    return nodes;
	  }

	  public void applyFormula(PGArc[] arcs, PGNode[] nodes, int iteration) {

	    // special case for default formula

	    if(formula == FORMULA_TFT) {
	      
	      for(int i = nodes.length; --i >= 0;) {

		PGNode n = nodes[i];
		n.sim = (n.simN = n.simN1) + n.sim0;
	      }
	      propagateValues(arcs);
	      return;
	    }

	    // generic, for all formulas
	    
	    //System.out.println(formula[0]);
	    //System.out.println(formula[1]);
	    //System.out.println(formula[2]);

	    boolean add_sigma0_before = formula[0];
	    boolean add_sigma0_after = formula[1];
	    boolean add_sigmaN_after = formula[2];
	    
	    //System.out.println(nodes.length);

	    for(int i = nodes.length; --i >= 0;) {
	      
	      PGNode n = nodes[i];
	      //System.out.println(nodes[i]);
	      // move simN1 values in simN and take current value from previous iteration
	      n.sim = n.simN = n.simN1;
	      
	      //System.out.println(n.sim0);
	      
	      if(add_sigma0_before)
		n.sim += n.sim0;
	    //System.out.println(n.sim);	      
	      // initialize simN1 for next iteration
	      if(!add_sigmaN_after)
		n.simN1 = 0; // otherwise, n.simN1 = n.sim from above
	      //System.out.println(n.simN1);

	      if(add_sigma0_after)
		n.simN1 += n.sim0;
	    }

//	     if(DEBUG && iteration < DEBUG_MAX_ITERATIONS) {
//	       System.err.println("\nBefore propagation: " + iteration);
//	       dump(nodes);
//	     }
	    
	    //System.out.println(arcs);

	    propagateValues(arcs);

	    if(DEBUG && iteration < DEBUG_MAX_ITERATIONS) {
	      System.err.println("\nAfter propagation: " + iteration);
	      dump(nodes);
	    }

	    /*
	    if(add_sigma0_after || add_sigmaN_after) {

	      for(int i = nodes.length; --i >= 0;) {
	      
		PGNode n = nodes[i];

		if(add_sigma0_after)
		  n.simN1 += n.sim0;

		if(add_sigmaN_after)
		  n.simN1 += n.sim;
	      }
	    }
	    */
	  }

	  public static void propagateValues(PGArc[] arcs) {

	    // propagate values from previous iteration over propagation graph
      //System.out.println(arcs);
	    for(int i = arcs.length; --i >= 0;) {

	      PGArc arc = arcs[i];
	      //System.out.println(arcs[i]);
	      //System.out.println(arc);                // print statement1
	      // forward
	      //System.out.println(arc.src.sim);
	      //System.out.println(arc.fw);
	      arc.dest.simN1 += arc.src.sim * arc.fw;
	      //System.out.println(arc.dest.simN1);
	      // backward
	      arc.src.simN1 += arc.dest.sim * arc.bw;
	      //System.out.println(arc.src.simN1);
	      //System.out.println(arc.dest.sim);       // print statement2
	      //System.out.println(arc.bw);           // print statement3
	      //System.out.println(arc.dest.simN1);
	      
	      //System.out.println(arc.src.simN1);     // print statement4
	    }
	  }

	  public double distance(PGNode[] nodes) {

	    double diff = 0.0;

	    for(int i = nodes.length; --i >= 0;) {
	      double d = nodes[i].simN1 - nodes[i].simN;
	      diff += d*d;
	    }

	    return Math.sqrt(diff);
	  }

	  public double distanceF(PGNode[] nodes, double maxN, double maxN1) {

	    if(DEBUG)
	      System.err.println("Calc distance with maxN=" + maxN + ", maxN1=" + maxN1);

	    double diff = 0.0;

	    for(int i=0; i < nodes.length; i++) {
	      double d = nodes[i].simN1 / maxN1 - nodes[i].simN / maxN;
	      diff += d*d;
	    }

	    return Math.sqrt(diff);
	  }

	  static double minN(PGNode[] nodes) {
	    
	    double min = 0;
	    for(int i=0; i < nodes.length; i++)
	      if(nodes[i].simN > 0)
		min = Math.min(min, nodes[i].simN);
	    return min;
	  }

	  static double maxN1(PGNode[] nodes) {
	    
	    double max = 0;
	    for(int i=0; i < nodes.length; i++)
	      max = Math.max(max, nodes[i].simN1);
	    return max;
	  }

	  static double sumN1(PGNode[] nodes) {
	    
	    double sum = 0;
	    for(int i=0; i < nodes.length; i++)
	      sum += nodes[i].simN1;
	    return sum;
	  }

	  static double sumN(PGNode[] nodes) {
	    
	    double sum = 0;
	    for(int i=0; i < nodes.length; i++)
	      sum += nodes[i].simN;
	    return sum;
	  }

	  static void normalizeN1(PGNode[] nodes) {
	    
	    double max = maxN1(nodes);
	    if(max == 0)
	      return;
	    for(int i=0; i < nodes.length; i++)
	      nodes[i].simN1 /= max;
	    //System.out.println(nodes);
	  }

	  public static void dump(Collection c) {

	    /*
		  for(Iterator it = c.iterator(); it.hasNext();)
	       
	       System.err.println(String.valueOf(it.next()));
	    */
	    /*
	    try {
			System.setOut(new PrintStream(new FileOutputStream("output_simi.txt")));
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	   */
		//  File fileerror = new File("/home/archana/ve/FA_feat_ASAG/gap_rem_err_codew/delete_iteration/FA_err1.txt");  
	    //File fileerror = new File("/home/archana/ve/FA_feat_ASAG/exclude_ie/delete_iteration/FA_err1.txt"); // this is default
	    //File fileerror = new File("./delete_iteration/FA_err1.txt"); // this is default
	    
	    //File fileerror = new File("/home/archana/ve/FA_feat_ASAG/code_write/delete_iteration/FA_err1.txt"); // this is default
	    //File fileerror = new File("/home/archana/ve/FA_feat_ASAG/code_write/delete_iteration/FA_err2.txt"); // this is default
	    File fileerror = new File("/home/archana/eclipse-workspace/graph_match/FA_err1.txt"); // this is default
	    //File fileerror = new File("/home/archana/FA_feat_ASAG/trial_directedFA/delete_files_iteration/FA_err.txt");
		FileOutputStream fos;
		try {
			fos = new FileOutputStream(fileerror);
			PrintStream ps = new PrintStream(fos);
			System.setErr(ps);

		} catch (FileNotFoundException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		//PrintStream ps = new PrintStream(fos);
		//System.setErr(ps);
		
		for(Iterator it = c.iterator(); it.hasNext();)
		       
		       System.err.println(String.valueOf(it.next()));

		//System.err.println("This goes to err.txt");

		/*try {
			throw new Exception("Exception goes to err.txt too");
		} catch (Exception e) {
			e.printStackTrace();
		}
	    
	    */
	    
	  }

	  public static void dump(Object[] arr) {

	    dump(Arrays.asList(arr));
	  }

	  PGNode getNormalNode(RDFNode n1, RDFNode n2) {

	    double sim = n1.equals(n2) ? 1.0 : MIN_NODE_SIM2;

	    boolean isL1 = n1 instanceof Literal;
	    boolean isL2 = n2 instanceof Literal;

	    if(isL1 != isL2)
	      sim *= StringMatcher.RESOURCE_LITERAL_MATCH_PENALTY;

	    PGNode node = new PGNode(n1, n2);
	    node.sim0 = sim;
	    return node;
	  }

	  // precompute pairs of statements to consider
	  // also computes sigma0 for the cross-product of all nodes and literals if needed
	  // computes a mapping, in principle

	  void initSigma0() throws ModelException {

	    System.err.println("All nodes are considered equally similar");
	    //    sigma0 = new HashSet();
	    Collection c2 = RDFUtil.getNodes(m2).values();
	    Iterator it1 = RDFUtil.getNodes(m1).values().iterator();
	    while(it1.hasNext()) {
	      RDFNode n1 = (RDFNode)it1.next();
	      Iterator it2 = c2.iterator();
	      while(it2.hasNext()) {
		RDFNode n2 = (RDFNode)it2.next();
		//	MapPair p = getNormalPair(n1, n2);
		//	System.err.println("Reinforce pair: " + p);
		//	sigma0.add(p);
		PGNode pn = getNormalNode(n1, n2);
		//	System.err.println("Init node: " + pn);
		pgnodes.put(pn, pn);
	      }
	    }
	  }


	  void constructPropagationGraph(boolean ignorePredicates) throws ModelException {

	    // SP -> count
	    Map cardMapSPLeft, cardMapOPLeft, cardMapPLeft, cardMapSPRight, cardMapOPRight, cardMapPRight;

	    cardMapSPLeft = new HashMap();
	    cardMapOPLeft = new HashMap();
	    cardMapPLeft = new HashMap();

	    cardMapSPRight = new HashMap();
	    cardMapOPRight = new HashMap();
	    cardMapPRight = new HashMap();

	    computeCardMaps(m1, cardMapSPLeft, cardMapOPLeft, cardMapPLeft, ignorePredicates); //no.of nodes going out of a node
	    computeCardMaps(m2, cardMapSPRight, cardMapOPRight, cardMapPRight, ignorePredicates);


	    Map outgoing = new HashMap(); // same as incoming
	    //    Map incoming = new HashMap();

	    List stmtPairs = new ArrayList();

	    for(Enumeration en1 = m1.elements(); en1.hasMoreElements();) {

	      Statement st1 = (Statement)en1.nextElement();
	      
	      if(st1.subject() instanceof Statement ||
		 st1.object() instanceof Statement)
		continue;

	      for(Enumeration en2 = m2.elements(); en2.hasMoreElements();) {

		Statement st2 = (Statement)en2.nextElement();

		if(st2.subject() instanceof Statement ||
		   st2.object() instanceof Statement)
		  continue;

//	 	if(tryAll) {
//	 	  sigma0.add(getNormalPair(st1.subject(), st2.subject()));
//	 	  sigma0.add(getNormalPair(st1.object(), st2.object()));
//	 	  sigma0.add(getNormalPair(st1.subject(), st2.object()));
//	 	  sigma0.add(getNormalPair(st1.object(), st2.subject()));
//	 	}

		double ps = 0.0; //predicateSim(st1.predicate(), st2.predicate());
		//	System.err.println("-- " + st1 + " -- " + st2);
		//System.out.println(st1.predicate());
		//System.out.println(st2.predicate());
		if(st1.predicate().equals(st2.predicate()))
		  ps = EQUAL_PRED_COEFF;
		else if(TRY_ALL_ARCS)
		  ps = OTHER_PRED_COEFF;

      //System.out.println(ps);  // predicate coeff are 1.0 if same pred otherwise 0.0
		if(ps > 0) {
		  //	  System.err.println("--- ps=" + ps + " from " + EQUAL_PRED_COEFF + ", " + TRY_ALL_ARCS + ", " + OTHER_PRED_COEFF);
		  StmtPair p = new StmtPair(st1, st2, ps,
					    getCard(cardMapSPLeft, st1.subject(), ignorePredicates ? null : st1.predicate()),
					    getCard(cardMapOPLeft, st1.object(), ignorePredicates ? null : st1.predicate()),
					    getCard(cardMapPLeft, null, ignorePredicates ? null : st1.predicate()),
					    getCard(cardMapSPRight, st2.subject(), ignorePredicates ? null : st2.predicate()),
					    getCard(cardMapOPRight, st2.object(), ignorePredicates ? null : st2.predicate()),
					    getCard(cardMapPRight, null, ignorePredicates ? null : st2.predicate())
					    );

//	 	  MapPair p = new MapPair(st1, st2, ps);
        //System.out.println(p);
		  if(FLOW_GRAPH_TYPE == FG_STOCHASTIC || FLOW_GRAPH_TYPE == FG_INCOMING) {

		    // collect the numbers

		    MapPair sourcePair = get(outgoing, st1.subject(), st2.subject());
		    sourcePair.sim += 1.0;
		    
	  	    sourcePair = get(outgoing, st1.object(), st2.object());
	  	    sourcePair.sim += 1.0;

		    if(TRY_ALL_ARCS) {
		      sourcePair = get(outgoing, st1.subject(), st2.object());
		      sourcePair.sim += 1.0;

		      sourcePair = get(outgoing, st1.object(), st2.subject());
		      sourcePair.sim += 1.0;
		    }

//	  	    MapPair targetPair = get(incoming, st1.object(), st2.object());
//	  	    targetPair.sim += 1.0;
		  }

		  if(DEBUG)
		    System.err.println("" + p);
		  stmtPairs.add(p);
		}
	      }
	    }

	    //System.out.println(stmtPairs);
	    if(FLOW_GRAPH_TYPE == FG_STOCHASTIC) {

	      Iterator it = stmtPairs.iterator();
	      while(it.hasNext()) {

		StmtPair p = (StmtPair)it.next();
		p.soso = 1.0 / get(outgoing, p.stLeft.subject(), p.stRight.subject()).sim;
		p.osos = 1.0 / get(outgoing, p.stLeft.object(), p.stRight.object()).sim;
		//System.out.println(p);
		if(TRY_ALL_ARCS) {
		  p.soos = 1.0 / get(outgoing, p.stLeft.subject(), p.stRight.object()).sim;
		  p.osso = 1.0 / get(outgoing, p.stLeft.object(), p.stRight.subject()).sim;
		}
		if(DEBUG)
		  System.err.println("Adjusted: " + p);
	      }
	    } else if(FLOW_GRAPH_TYPE == FG_INCOMING) {

	      Iterator it = stmtPairs.iterator();
	      while(it.hasNext()) {
		
		StmtPair p = (StmtPair)it.next();
		p.osos = 1.0 / get(outgoing, p.stLeft.subject(), p.stRight.subject()).sim;
		p.soso = 1.0 / get(outgoing, p.stLeft.object(), p.stRight.object()).sim;
		if(TRY_ALL_ARCS) {
		  p.osso = 1.0 / get(outgoing, p.stLeft.subject(), p.stRight.object()).sim;
		  p.soos = 1.0 / get(outgoing, p.stLeft.object(), p.stRight.subject()).sim;
		}
		if(DEBUG)
		  System.err.println("Adjusted: " + p);
	      }
	    }

	    // we don't need cardMaps any more, free memory
	    cardMapSPLeft = cardMapOPLeft = cardMapSPRight = cardMapOPRight = cardMapPLeft = cardMapPRight = null;


//	     pgnodes = new HashMap();
//	     pgarcs = new ArrayList();

	    for(Iterator it = stmtPairs.iterator(); it.hasNext();) {

	      StmtPair p = (StmtPair)it.next();
	      Statement st1 = (Statement)p.stLeft;
	      Statement st2 = (Statement)p.stRight;

	      PGNode ss = getNode(pgnodes, st1.subject(), st2.subject());
	      PGNode oo = getNode(pgnodes, st1.object(), st2.object());

	      pgarcs.add(new PGArc(ss, oo, p.soso * UPDATE_GUESS_WEIGHT, p.osos * UPDATE_GUESS_WEIGHT));

	      if(!DIRECTED_GRAPH) {

		PGNode so = getNode(pgnodes, st1.subject(), st2.object());
		PGNode os = getNode(pgnodes, st1.object(), st2.subject());

		pgarcs.add(new PGArc(so, os, p.soos * UPDATE_GUESS_WEIGHT, p.osso * UPDATE_GUESS_WEIGHT));
	      }
	    }
	    //System.out.println(pgarcs);
	  }


	  PGNode getNode(Map table, RDFNode r1, RDFNode r2) {

	    PGNode p = new PGNode(r1, r2);
	    PGNode res = (PGNode)table.get(p);
	    if(res == null) {
	      table.put(p, p);
	      return p;
	    }
	    return res;
	  }
	  
	  int getCard(Map cardMap, RDFNode r, Resource pred) {

	    MapPair p = get(cardMap, r, pred);
	    // there MUST be a pair after computeCardMaps!!!
	    return (int)p.sim;
	  }

	  // collects the number of nodes going out of a node

	  void computeCardMaps(Model m, Map cardMapSP, Map cardMapOP, Map cardMapP, boolean ignorePredicates) throws ModelException {

	    for(Enumeration en = m.elements(); en.hasMoreElements();) {

	      Statement st = (Statement)en.nextElement();
	      
	      if(st.subject() instanceof Statement ||
		 st.object() instanceof Statement)
		continue;

	      Resource pred = ignorePredicates ? null : st.predicate();
	      MapPair p = get(cardMapSP, st.subject(), pred);
	      p.sim += 1.0;
	      
	      p = get(cardMapOP, st.object(), pred);
	      p.sim += 1.0;

	      p = get(cardMapP, null, pred);
	      p.sim += 1.0;
	    }
	  }

	  MapPair get(Map table, RDFNode r1, RDFNode r2) {

	    MapPair p = setPair(GET_PAIR, r1, r2); // new MapPair(r1, r2); //
	    // MapPair p = new MapPair(r1, r2);
	    MapPair res = (MapPair)table.get(p);
	    if(res == null) {
	      res = p.duplicate();
	      table.put(res, res);
	    }
	    return res;
	  }

	  // this method is used to avoid creating of new objects
	  MapPair setPair(int id, RDFNode r1, RDFNode r2) {

	    MapPair p = cachePairs[id];
	    p.setLeft(r1);
	    p.setRight(r2);
	    //    p.hash = 0;
	    return p;
	  }

	  public int getMinInputLen() { return 2; }

	  public int getMaxInputLen() { return 3; }

	  public int getMinOutputLen() { return 1; }

	  public int getMaxOutputLen() { return 1; }


	  /**
	   * A node in the propagation graph
	   */
	  class PGNode extends MapPair {

	    double sim0;
	    // double sim; corresponds to simN, defined in MapPair
	    double simN1; // N+1
	    double simN; // for comparing vectors, storage only

	    public PGNode(Object r1, Object r2) {

	      super(r1, r2);
	    }

	    public String toString() {

	      return "[" + getLeft() + "," + getRight() + ": sim=" + sim + ", init=" + sim0 + ", N=" + simN + ", N1=" + simN1 + (inverse ? ", inverse" : "") + "]";
	    }
	  }

	  /**
	   * An arc of the propagation graph
	   */
	  class PGArc {

	    double fw, bw; // coefficients on arcs
	    PGNode src, dest;

	    public PGArc(PGNode n1, PGNode n2, double fw, double bw) {

	      this.src = n1;
	      this.dest = n2;
	      this.fw = fw;
	      this.bw = bw;
	    }

	    public String toString() {

	      return src + " <--" + bw + " " + fw + "--> " + dest;
	    }
	  }

	  /**
	   * Instances of this class are used temporarily for creating the propagation graph
	   */
	  class StmtPair {

	    Statement stLeft, stRight;
	    double predSim;
	    //    int spLeft,opLeft,spRight,opRight;
	    double soso,osos,soos,osso;

	    public StmtPair(Statement stLeft, Statement stRight, double predSim,
			    int spLeft, int opLeft, int pLeft, int spRight, int opRight, int pRight) {

	      //      System.err.println("--- predSim=" + predSim);

	      this.stLeft = stLeft;
	      this.stRight = stRight;
	      this.predSim = predSim;

	      switch(FLOW_GRAPH_TYPE) {

	      case match1.FG_AVG: {

		double c = 2.0;
		this.soso = c * predSim / (spLeft + spRight);
		this.osos = c * predSim / (opLeft + opRight);
		this.soos = c * predSim / (spLeft + opRight);
		this.osso = c * predSim / (opLeft + spRight);
		//	System.err.println("--- soso=" + soso + " from predSim=" + predSim + ", spLeft="+ spLeft + ", spRight=" + spRight);
		break;
	      }
	      case match1.FG_PRODUCT: {

		double c = 1.0;
		this.soso = c * predSim / (spLeft * spRight);
		this.osos = c * predSim / (opLeft * opRight);
		this.soos = c * predSim / (spLeft * opRight);
		this.osso = c * predSim / (opLeft * spRight);
		break;
	      }

		/*
	      case Match.FG_CONSTANT_WEIGHT: { // ignore directionality

		double c = 1.0 / ((spLeft * spRight) + (opLeft * opRight));
		this.soso = c * predSim;
		this.osos = c * predSim;
		this.soos = c * predSim;
		this.osso = c * predSim;
		break;
	      }
		*/
	      case match1.FG_EQUAL:
	      case match1.FG_INCOMING:
	      case match1.FG_STOCHASTIC: { // for constant weight, weight computed here does not matter...

		double c = 1.0;
		this.soso = c * predSim;
		this.osos = c * predSim;
		this.soos = c * predSim;
		this.osso = c * predSim;
		break;
	      }
	      case match1.FG_TOTALP: {

		double c = pLeft * pRight;
		this.soso = predSim / c;
		this.osos = predSim / c;
		this.soos = predSim / c;
		this.osso = predSim / c;
		break;
	      }
	      case match1.FG_TOTALS: {

		double c = 2.0 / (pLeft + pRight);
		this.soso = predSim * c;
		this.osos = predSim * c;
		this.soos = predSim * c;
		this.osso = predSim * c;
		break;
	      }

	      case match1.FG_AVG_TOTALS: {

		double c = 4.0 / (pLeft + pRight);
		this.soso = c * predSim / (spLeft + spRight);
		this.osos = c * predSim / (opLeft + opRight);
		this.soos = c * predSim / (spLeft + opRight);
		this.osso = c * predSim / (opLeft + spRight);
		break;
	      }

	      }
	    }

	    public String toString() {


	      try {
		return "StmtPair[(" + stLeft.subject() + "," + stRight.subject() + ") -> (" +
		  stLeft.object() + "," + stRight.object() + "), " + soso + "->, <-" + osos +
		  (TRY_ALL_ARCS ? " *** (" + stLeft.subject() + "," + stRight.object() + ") -> (" +
		   stLeft.object() + "," + stRight.subject() + "), " + soos + "->, <-" + osso + ")" : "");
	      } catch (ModelException any) {
		return "StmtPair[" + stLeft + "," + stRight + "," + predSim + "," +
		  soso + "," + osos + "," + soos + "," + osso;
	      }
	    }
	  }

	  /*
	  public class Triplet<T, U, V> {

		    private final T first;
		    private final U second;
		    private final V third;

		    public Triplet(T first, U second, V third) {
		        this.first = first;
		        this.second = second;
		        this.third = third;
		    }

		    public T getFirst() { return first; }
		    public U getSecond() { return second; }
		    public V getThird() { return third; }
		}

*/
	  /*
	  class Pair<A,B> {
		    A a;
		    B b;
		    public Pair( A a, B b ) {
		        this.a = a;
		        this.b = b;
		    } 
		}
	  */
	  /*
	  class Triples<A,B,C> {
		    A a;
		    B b;
		    C c;
		    public Triples( A a, B b , C c) {
		        this.a = a;
		        this.b = b;
		        this.c = c;
		    } 
		}
		*/
	  
	  
	/*
	  public static class Combination {
		  
		  public static String[] combination(Object[]  elements, int K){
		   
		          // get the length of the array
		          // e.g. for {'A','B','C','D'} => N = 4 
		          int N = elements.length;
		           
		          if(K > N){
		              System.out.println("Invalid input, K > N");
		              return new String[0];
		          }
		          // calculate the possible combinations
		          // e.g. c(4,2)
		          //c(N,K);
		           
		          // get the combination by index 
		          // e.g. 01 --> AB , 23 --> CD
		          int combination[] = new int[K];
		           
		          // position of current index
		          //  if (r = 1)              r*
		          //  index ==>        0   |   1   |   2
		          //  element ==>      A   |   B   |   C
		          int r = 0;      
		          int index = 0;
		           
		          while(r >= 0){
		              // possible indexes for 1st position "r=0" are "0,1,2" --> "A,B,C"
		              // possible indexes for 2nd position "r=1" are "1,2,3" --> "B,C,D"
		               
		              // for r = 0 ==> index < (4+ (0 - 2)) = 2
		              if(index <= (N + (r - K))){
		                      combination[r] = index;
		                       
		                  // if we are at the last position print and increase the index
		                  if(r == K-1){
		   
		                      //do something with the combination e.g. add to list or print
		                      //print(combination, elements);
		                      index++;                
		                  }
		                  else{
		                      // select index for next position
		                      index = combination[r]+1;
		                      r++;                                        
		                  }
		                  //System.out.println(index);
		              }
		              else{
		                  r--;
		                  if(r > 0)
		                      index = combination[r]+1;
		                  else
		                      index = combination[0]+1;  
		                  //System.out.println(index);
		              }           
		          }
				return null;
		      }
		  }
	  
	  */
	  
	  //public class Combinations {
		  /*
		    public static void main(String[] args) {
		        int[] arr = {1, 2, 3, 4, 4, 5};
		        int r = 3;
		        Arrays.sort(arr);
		        combine(arr, r);
		    }
		    */
	  
	  /*

		    private static void combine(String[] arr, int r) {
		        String[] res = new String[r];
		        doCombine(arr, res, 0, 0, r);
		    }



		    private static void doCombine(String[] arr, String[] res, int currIndex, int level, int r) {
		        if(level == r){
		            printArray(res);
		            return;
		        }
		        for (int i = currIndex; i < arr.length; i++) {
		            res[level] = arr[i];
		            doCombine(arr, res, i+1, level+1, r);
		            //way to avoid printing duplicates
		            if(i < arr.length-1 && arr[i] == arr[i+1]){
		                i++;
		            }
		        }
		    }

		    private static void printArray(String[] res) {
		        for (int i = 0; i < res.length; i++) {
		            System.out.print(res[i] + " ");
		        }
		        System.out.println();
		    }
	*/
	  
	  //public class CartesianProduct {
		  
		    public List<?> product(List<?>... a) {
		        if (a.length >= 2) {
		            List<?> product = a[0];
		            for (int i = 1; i < a.length; i++) {
		                product = product(product, a[i]);
		            }
		            return product;
		        }
		 
		        return emptyList();
		    }
		 
		    private static <A, B> List<?> product(List<A> a, List<B> b) {
		        return of(a.stream()
		                .map(e1 -> of(b.stream().map(e2 -> asList(e1, e2)).collect(toList())).orElse(emptyList()))
		                .flatMap(List::stream)
		                .collect(toList())).orElse(emptyList());
		    }
		//}
		    
		    static void ICDE02Example(String[] args) throws Exception {
		    	//static void ICDE02Example() throws Exception {	
		    		if(args.length > 0) {
		            File file = new File(args[0]);  // this is default
		    	    //File file = new File("/home/archana/ve/FA_feat_ASAG/exclude_ie/delete_iteration/woutm_2new.txt");
		            
		    		//File file = new File("/home/archana/ve/FA_feat_ASAG/gap_rem_err_codew/delete_iteration/woutm_2new.txt");
		    		//previous File file = new File("/home/archana/ve/FA_feat_ASAG/code_write/delete_iteration/woutm_2new.txt");
		    		
		    		//File file = new File("/home/archana/FA_directed/graph_5.txt");
		    		//File file = new File("/home/archana/FA_feat_ASAG/trial_directedFA/delete_files_iteration/woutm_2new.txt");
		    		//File file = new File("/home/archana/FA_feat_ASAG/trial_directedFA/delete_files_iteration/m_1.txt");
		    		 
		    		BufferedReader br = new BufferedReader(new FileReader(file));
		    		 
		    		String st;
		    		String stnew = "";
		    		
		    		RDFFactory rf = new RDFFactoryImpl();
		    		NodeFactory nf = rf.getNodeFactory();
		    		 
		    				
		    		Model A = rf.createModel();	
		    		
		    		List triple_ver = new ArrayList();
		    		List only_verA = new ArrayList();
		    		
		    		while ((st = br.readLine()) != null)
		    		    //System.out.println(st);
		    		{
		    		     //stnew = stnew + st+"\n";
		    		     //String [] arrOfStr = stnew.split("  ");
		    			 List list_graph = new ArrayList();
		    			 String [] arrOfStr = st.split("\\t");
		    			    
		    			 for (String a : arrOfStr)
		    		         //System.out.println(a);
		    			     list_graph.add(a);
		    			 
		    			 //System.out.println(list_graph);
		    			 
		    			// System.out.println(list_graph);
		    			 
		    			 //RDFFactory rf = new RDFFactoryImpl();
		    			 //NodeFactory nf = rf.getNodeFactory();
		    			 
		    			 
		    			 /*
		    			 List all_resource = new ArrayList();
		    			    for (int i =0; i < list_graph.size(); i++) {
		    			    	Resource r = nf.createResource((String) list_graph.get(i));
		    			    	all_resource.add(r);
		    			    }  
		    			    
		    			 System.out.println(all_resource);
		    			 */
		    			 
		    			 Resource r1 = nf.createResource((String) list_graph.get(0));
		    			 Resource r2 = nf.createResource((String) list_graph.get(1));
		    			 Resource r3 = nf.createResource((String) list_graph.get(2));
		    			 //Model A = rf.createModel();
		    			 
		    			 //String[] names = new String[] {"john", "doe", "anne"};
		    			// String[] names = new String[] (all_resource);
		    			 /*
		    			 String[] stringArray = (String[]) all_resource.toArray(new String[0]);
		    			 System.out.println(stringArray);
		    			 
		    			 Triplet<String, String, String> triplet2 = Triplet.fromArray(stringArray);
		    			 */
		    			 /*
		    		     Object[] array = all_resource.toArray();
		    			 System.out.println(array);
		    			 */
		    			 A.add(nf.createStatement(r1, r2, r3));
		    			 List all_resource = new ArrayList();
		    			 all_resource.add(r1);
		    			 //all_resource.add(r2);
		    			 all_resource.add(r3);
		    			 triple_ver.add(all_resource);
		    			 only_verA.add(r1);
		    			 only_verA.add(r3);
		    			 
		    			 
		    			 //product(r1, r3);
		    			 
		    			 //String[] stringArray = (String[]) all_resource.toArray();
		    			 //System.out.println(all_resource);
		    			 //Arrays.sort(all_resource);
		    		     //combine(stringArray, 2);
		    			 
		    			 //Combination.combination(stringArray,2);
		    			 
		    			 
		    		}
		    		//System.out.println(triple_ver);
		    		
		    		//File file2 = new File("/home/archana/ve/FA_feat_ASAG/exclude_ie/delete_iteration/wouts_2new.txt");
		    		File file2 = new File(args[1]);   // this is default
		    		//File file2 = new File("/home/archana/ve/FA_feat_ASAG/gap_rem_err_codew/delete_iteration/wouts_2new.txt");
		    		//previous File file2 = new File("/home/archana/ve/FA_feat_ASAG/code_write/delete_iteration/wouts_2new.txt");
		    		
		    		//File file2 = new File("/home/archana/FA_feat_ASAG/trial_directedFA/delete_files_iteration/wouts_2neww.txt");
		    		//File file2 = new File("/home/archana/FA_feat_ASAG/trial_directedFA/delete_files_iteration/wouts_2new.txt");
		    		//File file2 = new File("/home/archana/FA_feat_ASAG/trial_directedFA/delete_files_iteration/s_1.txt");
		    		 
		    		BufferedReader br2 = new BufferedReader(new FileReader(file2));
		    		
		            Model B = rf.createModel();	
		    		
		    		List triple_verB = new ArrayList();
		    		
		    		//List only_verA = new ArrayList();
		    		List only_verB = new ArrayList();
		    		

		    		while ((st = br2.readLine()) != null)
		    		    //System.out.println(st);
		    		{
		    		     //stnew = stnew + st+"\n";
		    		     //String [] arrOfStr = stnew.split("  ");
		    			 List list_graph = new ArrayList();
		    			 String [] arrOfStr = st.split("\\t");
		    			    
		    			 for (String a : arrOfStr)
		    		         //System.out.println(a);
		    			     list_graph.add(a);
		    			 
		    			 //System.out.println(list_graph);
		    			 
		    			// System.out.println(list_graph);
		    			 
		    			 //RDFFactory rf = new RDFFactoryImpl();
		    			 //NodeFactory nf = rf.getNodeFactory();
		    			 
		    			 
		    			 /*
		    			 List all_resource = new ArrayList();
		    			    for (int i =0; i < list_graph.size(); i++) {
		    			    	Resource r = nf.createResource((String) list_graph.get(i));
		    			    	all_resource.add(r);
		    			    }  
		    			    
		    			 System.out.println(all_resource);
		    			 */
		    			 
		    			 Resource r1 = nf.createResource((String) list_graph.get(0));
		    			 Resource r2 = nf.createResource((String) list_graph.get(1));
		    			 Resource r3 = nf.createResource((String) list_graph.get(2));
		    			 //Model A = rf.createModel();
		    			 
		    			 //String[] names = new String[] {"john", "doe", "anne"};
		    			// String[] names = new String[] (all_resource);
		    			 /*
		    			 String[] stringArray = (String[]) all_resource.toArray(new String[0]);
		    			 System.out.println(stringArray);
		    			 
		    			 Triplet<String, String, String> triplet2 = Triplet.fromArray(stringArray);
		    			 */
		    			 /*
		    		     Object[] array = all_resource.toArray();
		    			 System.out.println(array);
		    			 */
		    			 B.add(nf.createStatement(r1, r2, r3));
		    			 List all_resource = new ArrayList();
		    			 all_resource.add(r1);
		    			 //all_resource.add(r2);
		    			 all_resource.add(r3);
		    			 triple_verB.add(all_resource);
		    			 
		    			 only_verB.add(r1);
		    			 only_verB.add(r3);
		    			 
		    			 //product(r1, r3);
		    			 
		    			 //String[] stringArray = (String[]) all_resource.toArray();
		    			 //System.out.println(all_resource);
		    			 //Arrays.sort(all_resource);
		    		     //combine(stringArray, 2);
		    			 
		    			 //Combination.combination(stringArray,2);
		    			 
		    			 
		    		}
		    		
		    		//System.out.println(A);
		    		//System.out.println(B);
		    		//System.out.println(triple_ver);
		    		//System.out.println(triple_verB);
		    		
		    		//String[] A1 = {"art", "beauty", "beautiful", "make-up"};
		    		//String[] B1 = {"art1", "beauty1", "beautiful1", "make-up1"};
		    		
		    	//	List A2 = A1.toList();
		    		//List<String> A2 = Arrays.asList(A1);
		    		//List<String> B2 = Arrays.asList(B1);
		    		
		    		//System.out.println(only_verA);
		    		//System.out.println(only_verB);
		    		
		    		//System.out.println(product(only_verA, only_verB));
		    		
		    		List pp = product(only_verA, only_verB);
		    		
		    		List all_pairs = new ArrayList();
		    		
		    		for (int i =0; i < pp.size(); i++) {
		    	    	Object r = pp.get(i);
		    	    	all_pairs.add(r);
		    	    }  
		    		
		    		//System.out.println(all_pairs);
		    		
		    		//List initMap = new ArrayList();
		    	    //initMap.add(new MapPair(a, b, 1.0));
		    		
		    		
		    		 //this part is important if all the pairs of vertices are to be assigned an initial similarity of 1.0 
		    /*		
//		    		///////////////////
		    		List initMap = new ArrayList();
		    		for (int i = 0; i < all_pairs.size(); i++) {
		    			//initMap.add(new MapPair(all_pairs.get(i)(0)))
		    			//String[] a1 = (String[]) all_pairs.get(i);
		    			List a11 = Arrays.asList(all_pairs.get(i)); 
		    			//System.out.println(a11);
		    			//System.out.println(a11.get(0));
		    			List arr1 = (List) a11.get(0);
		    			//System.out.println(arr1);
		    			//System.out.println(arr1.get(0));
		    			//System.out.println(arr1.get(1));
		    			
		    			initMap.add(new MapPair(arr1.get(0), arr1.get(1), 1.0));
		    			//System.out.println(((Map) a11.get(0)).get(0));
		    			//String a12 = a11.get(0).get(0);
		    			//ArrayList al1 = (ArrayList) a1;
		    			
		    			//System.out.println(a1);
		    			//List al1 = Arrays.asList(a1);
		    			//System.out.println(al1);
		    			//Object a2 = ((Map) a1).get(0);
		    			//Object a2 = ((Map) al1.get(0)).get(0);
		    			//Object al1 = a1[0];
		    			//System.out.println(al1);
		    		}
		    */		
//		    		 ///////////////////// above part imp for initializing 1.0 
		    		
		    		
		    /*		
		    		
		    		String pythonScriptPath = "/home/archana/workspace/try_java_py/script2.py";
		    		List initMap = new ArrayList();
		    		for (int i = 0; i < all_pairs.size(); i++) {
		    			//initMap.add(new MapPair(all_pairs.get(i)(0)))
		    			//String[] a1 = (String[]) all_pairs.get(i);
		    			List a11 = Arrays.asList(all_pairs.get(i)); 
		    			//System.out.println(a11);
		    			//System.out.println(a11.get(0));
		    			List arr1 = (List) a11.get(0);
		    			//System.out.println(arr1);
		    			//System.out.println(arr1.get(0));
		    			//System.out.println(arr1.get(1));
		    			
		    			String[] cmd = new String[4];
		    			cmd[0] = "python"; // check version of installed python: python -V
		    			cmd[1] = pythonScriptPath;
		    			//cmd[2] = (String) arr1.get(0);
		                Object rr = arr1.get(0);
		                String rr1 = rr.toString();
		                cmd[2] = rr1;
		                
		    			//cmd[3] = (String) arr1.get(1);
		    			Object rs = arr1.get(1);
		                String rs1 = rs.toString();
		                cmd[3] = rs1;
		                
		                //System.out.println(rr1);
		                //System.out.println(rs1);
		    			
		    			Runtime rt = Runtime.getRuntime();
		    			Process pr = rt.exec(cmd);
		    			 
		    			BufferedReader bfr = new BufferedReader(new InputStreamReader(pr.getInputStream()));
		    			String line = "";
		    			//System.out.println(bfr.readLine());
		    			while((line = bfr.readLine()) != null) {
		    			// display each output line form python script
		    			//System.out.println(line);
		    			


		                //System.out.println(line.getClass().getName());


		    			//initMap.add(new MapPair(arr1.get(0), arr1.get(1), 1.0));
		    			//float number = new Float(line).floatValue();
		    			//String ll = "0.429";
		    			float number = Float.parseFloat(line);
		    			System.out.println(number);
		    			initMap.add(new MapPair(arr1.get(0), arr1.get(1), number));
		    			//System.out.println(((Map) a11.get(0)).get(0));
		    			//String a12 = a11.get(0).get(0);
		    			//ArrayList al1 = (ArrayList) a1;
		    			
		    			//System.out.println(a1);
		    			//List al1 = Arrays.asList(a1);
		    			//System.out.println(al1);
		    			//Object a2 = ((Map) a1).get(0);
		    			//Object a2 = ((Map) al1.get(0)).get(0);
		    			//Object al1 = a1[0];
		    			//System.out.println(al1);
		    			}
		    		}
		    		
		    		
		    		///////// passing pair by pair to python code for similarity between phrases
		    */		
		    		
		    		List<ArrayList<String>> lol = new ArrayList<ArrayList<String>>();
		    		
		    		//System.out.println(all_pairs);
		    		
		    		for (int i = 0; i < all_pairs.size(); i++)
		    		{
		    			List a11 = Arrays.asList(all_pairs.get(i));
		    			List arr1 = (List) a11.get(0);
		    			Object rr = arr1.get(0);
		                String rr1 = rr.toString();
		                
		                Object rs = arr1.get(1);
		                String rs1 = rs.toString();
		                
		                ArrayList<String> anotherList = new ArrayList<String>();
		                
		                anotherList.add(rr1);
		                anotherList.add(rs1);
		                
		                lol.add(anotherList);
		                
		                
		                
		    		}
		    		
		    		//System.out.println(lol);
		    		
		    		//String pythonScriptPath = "./script3.py";
		    		//String pythonScriptPath = "/home/archana/ve/FA_feat_ASAG/exclude_ie/script3.py";
		    		String pythonScriptPath = "/home/archana/ve/FA_feat_ASAG/code_write/script3.py";
		    		//String pythonScriptPath = "/home/archana/ve/FA_feat_ASAG/gap_rem_err_codew/script3.py";
		    	
		    		String[] cmd = new String[3];
		    		cmd[0] = "python"; // check version of installed python: python -V
		    		cmd[1] = pythonScriptPath;
		    		String lol1 = lol.toString();
		    		cmd[2] = lol1;
		    		//System.out.println(lol1);
		    		
		    		
		    		Runtime rt = Runtime.getRuntime();
		    		Process pr = rt.exec(cmd);
		    		BufferedReader bfr = new BufferedReader(new InputStreamReader(pr.getInputStream()));
		    	
		    		//String lol1 = lol.toString();
		    		//Runtime rt = Runtime.getRuntime();
		    		//"python test1.py "+number1+" "+number2
		    		//Process pr = rt.exec("python /home/archana/workspace/try_java_py/script3.py" + lol);
		    		//BufferedReader bfr = new BufferedReader(new InputStreamReader(pr.getInputStream()));
		    		//System.out.println(bfr.readLine());
		    		String line = "";
		    		while((line = bfr.readLine()) != null) {
		    		
		    			//System.out.println(line);
		    			
		    			//String line = "0.429636194854,0.329024456292,0.429636194854,0.284976867886,0.429636194854,0.170173921144,0.557941655642,0.376472790143,0.454601346238,0.29843189768,0.454601346238,0.323743547686,0.454601346238,0.109001373166,0.494124365781,0.378436562169,0.429636194854,0.329024456292,0.429636194854,0.284976867886,0.429636194854,0.170173921144,0.557941655642,0.376472790143,0.388962838563,0.707337097032,0.388962838563,0.477695377909,0.388962838563,0.252484235757,0.465969893327,0.890346416526,0.429636194854,0.329024456292,0.429636194854,0.284976867886,0.429636194854,0.170173921144,0.557941655642,0.376472790143,0.338467637185,0.736822250721,0.338467637185,0.334320702441,0.338467637185,0.205942812215,0.446348304817,1.0";
		    			List<String> myList = new ArrayList<String>(Arrays.asList(line.split(",")));
		    			//System.out.println(myList);
		    		
		    		List initMap = new ArrayList();
		    		for (int i = 0; i < all_pairs.size(); i++) {
		    			
		    			List a11 = Arrays.asList(all_pairs.get(i)); 
		    			
		    			List arr1 = (List) a11.get(0);
		    			
		                Object rr = arr1.get(0);
		                String rr1 = rr.toString();
		                
		    			Object rs = arr1.get(1);
		                String rs1 = rs.toString();      

		                
		    			float number = Float.parseFloat(myList.get(i));
		    			//System.out.println(number);
		    			initMap.add(new MapPair(arr1.get(0), arr1.get(1), number));  // sending initial sim value of a map pair
		    			
		    		}
		    					            
		    		//System.out.println(initMap);
		     
		    	    match1 sf = new match1();

		    	    sf.formula = FORMULA_TTT;
		    	    //sf.formula = FORMULA_FFT;
		    	    //sf.formula = FORMULA_TFF;
		    	    sf.FLOW_GRAPH_TYPE = FG_PRODUCT;

		    	    MapPair[] result = sf.getMatch(A, B, initMap);
		    	    MapPair.sort(result);
		    	    //System.out.println(result);
		    	    dump(result);
		    	    
		    /*	    
		    	    public static void dump(Collection c) {

		    		    for(Iterator it = c.iterator(); it.hasNext();)
		    		      System.err.println(String.valueOf(it.next()));
		    		  }

		    		  public static void dump(Object[] arr) {

		    		    dump(Arrays.asList(arr));
		    		  }
		    		  */
		    	    //System.out.println(result);
		    	    
		    	    //PrintWriter writer = new PrintWriter("output_simi.txt", "UTF-8");
		    	    //writer.println("The first line");
		    	    //writer.println("The second line");
		    	    //writer.println(result);
		    	    //writer.close();
		    	    
		    	    /*
		    	    PrintWriter out = new PrintWriter(new FileWriter("output_simi.txt"));

		    	      //output to the file a line
		    	    out.println(result);

		    	      //close the file (VERY IMPORTANT!)
		    	    out.close();
		    	    
		    	    PrintStream printStream = new PrintStream(new FileOutputStream("output_simi.txt"));
		    	    System.setOut(printStream);
		    	    */
		    	    
		    	    //System.setOut(new PrintStream(new FileOutputStream("output_simi.txt")));
		    	    //System.out.println("This is test output");
		    	    //System.out.println(result);


		    	    
		    	    //    MapPair.printMap(Arrays.asList(result), System.out);
		    	    
		    	    }
		    		}
		    }
		    	
		    	  //}

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		try {
			ICDE02Example(args);
			//ICDE02Example();
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

}
