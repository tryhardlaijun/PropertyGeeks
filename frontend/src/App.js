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
					<Route path="/PMI" element={<Dashboard />} />
					<Route path="/login" element={<Login setToken={setToken} isLoggedIn = {isLoggedIn()}/>} />
					<Route path="/profile" element={<Dashboard />} />
					<Route path="/logout" element={<Logout />} />
					<Route path="/resale/:id" element={<Resale />} />
				</Routes>
			</BrowserRouter>
		</>
	);
}

export default App;
