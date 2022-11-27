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
