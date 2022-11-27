export FLASK_APP=main && flask run

//Get All Flat Types
http://127.0.0.1:5000/all/getFlatTypes

//Get All Quarters
http://127.0.0.1:5000/all/getQuarter

//Get All Region
http://127.0.0.1:5000/all/getRegion

//Get All Flats By FlatType or Region
http://127.0.0.1:5000/all/getFlatsByFilter
http://127.0.0.1:5000/flat/all/getFlatsByFilter?fid=7
http://127.0.0.1:5000/all/getFlatsByFilter?rid=7
http://127.0.0.1:5000/all/getFlatsByFilter?fid=7&rid=7

//Get Flat Details by Flat Detail ID
http://127.0.0.1:5000/filter/getFlatDetails?fd_id=22

//Get Flat Rental by Flat Detail ID
http://127.0.0.1:500/flat/filter/getFlatRental0/filter/getFlatRental?fd_id=33

//Get Flat Price by Flat Detail ID
http://127.0.0.1:5000/filter/getFlatPrice?fd_id=33

PMI
http://127.0.0.1:5001/pmi/all/getPropertyType
http://127.0.0.1:5001/pmi/all/getStreets
http://127.0.0.1:5001/pmi/all/getPMIByFilter
http://127.0.0.1:5001/pmi/all/getPMIByFilter?property_type=Condominium
http://127.0.0.1:5001/pmi/all/getPMIByFilter?project=1 KING ALBERT PARK
http://127.0.0.1:5001/pmi/all/getPMIByFilter?street=KING ALBERT PARK

http://127.0.0.1:5001/pmi/filter/getPMIRental?pmi_id=10

http://127.0.0.1:5001/pmi/filter/getPMISalesPrice?pmi_id=10