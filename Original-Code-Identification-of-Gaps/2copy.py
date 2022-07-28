f = open('/location-to-store-output-files/pro_opm.txt', 'r')
f2 = open('/location-to-store-output-files/1_inp1.txt', 'a')
f1 = f.readlines()

for line in f1:
    line_1 = line.split(".")
	
    mm = []

   

    if "\n" in line_1:
       line_1.remove("\n")

    if "" in line_1:
       line_1.remove("")
    
    
    for ii in line_1:   # ii is each sentence in a line. 
	ii1 = ii.split(" ")
        
        if "" in ii1:
           ii1.remove("")
        
	ll = []
        
	ll.append(ii1[0].capitalize())
	for yy in ii1[1:]:
	    yy1 = yy.lower()
	    ll.append(yy1)
        ll.append(".")
			
	
			
	ll1 = " ".join(ll[:])
	mm.append(ll1)
	    
	 
    mm1 = " ".join(mm[:])     	
		
    line1 = str(1)+'\t'+mm1
    
    line2 = str(line1)
    f2.write(line2)
f.close()
f2.close()
