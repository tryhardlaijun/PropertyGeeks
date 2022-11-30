import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Dashboard from "./components/Dashboard/Dashboard";
import Login from "./components/Login/Login";
import useToken from "./useToken";
import Navbar from "./components/Navbar/Navbar";
import "./index.css";
import Logout from "./components/Logout/Logout";
import HDB from "./components/HDB/HDB";
import Resale from "./components/HDB/Resale";
import PMI from "./components/PMI/PMI";
import PMIrent from "./components/PMI/PMIrental";
import PMIsale from "./components/PMI/PMIsale";
import SignupPage from "./components/Signup/Signup";
import PMISQL from "./components/PMI/PMIsql";
import PMIDetailsSQL from "./components/PMI/PMIDetailsSQL";
import HDBNOSQL from "./components/HDB/HDBNOSQL";
import SaleNoSql from "./components/HDB/SaleNoSQL";
import RentNoSql from "./components/HDB/RentalNoSQL";
import Bookmark from "./components/Login/Profile";
import UpdateBM from "./components/Login/UpdateBM";
import DelBM from "./components/Login/DelBM";


function App() {
	const { token, setToken } = useToken();

	const isLoggedIn = () =>{
		if(token){
			return true
		}
		return false
	}

	return (
		<>
			<BrowserRouter>
				<Navbar />
				<Routes>
					<Route path="/" element={<Dashboard />} />
					<Route path="/HDB" element={<HDB />} />
					<Route path="/HDBNOSQL" element={<HDBNOSQL />} />
					<Route path="/resale/:id" element={<Resale />} />
					<Route path="/HDBNOSQLSale/:id" element={<SaleNoSql />} />
					<Route path="/HDBNOSQLRent/:id" element={<RentNoSql />} />
					<Route path="/PMI" element={<PMISQL />} />
					<Route path="/PMINOSQL" element={<PMI />} />
					<Route path="/pmisaleSQl/:id" element={<PMIDetailsSQL />} />
					<Route path="/pmirental/:id" element={<PMIrent />} />
					<Route path="/pmisale/:id" element={<PMIsale />} />
					<Route path="/login" element={<Login setToken={setToken} isLoggedIn = {isLoggedIn()}/>} />
					<Route path="/profile" element={<Bookmark />} />
					<Route path="/updateBM/:bid/:uid" element={<UpdateBM />} />
					<Route path="/logout" element={<Logout isLoggedIn = {isLoggedIn()}/>} />
					<Route path="/signup" element={<SignupPage />} />
					<Route path="/delBM/:bid/:uid" element={<DelBM />} />
				</Routes>
			</BrowserRouter>
		</>
	);
}

export default App;
