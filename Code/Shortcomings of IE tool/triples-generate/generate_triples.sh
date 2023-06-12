./arkref.sh -input m.txt
python pro_reso33.py
python 2copy.py
java -jar clausie.jar -vlf /location-where-to-store-output-files/1_inp1.txt -o /location-where-to-store-output-files/outm.txt
./arkref.sh -input s1.txt
python pro_reso3.py
python 3copy1_2.py
java -jar clausie.jar -vlf /location-where-to-store-output-files/2_inp1.txt -o /location-where-to-store-output-files/outs.txt
python triples_extract_ie.py
