import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import PropTypes from "prop-types";
import axios from "axios";

async function loginUser(credentials) {
	try {
		const response = await axios.post("http://127.0.0.1:5000/loginAPI",credentials);
		console.log(response);
		const token = await response.data.token;
		return token;
	} catch (error) {
		const message = `An error occurred: ${error}`;
		window.alert(message);
		return;
	}
}

export default function Login({ setToken , isLoggedIn}) {
	const [form, setForm] = useState({
		username:"",
		password:""
	});
	const navigate = useNavigate();
	const handleSubmit = async (e) => {
		const newPerson = {...form}
		e.preventDefault();
		const token = await loginUser(newPerson);
		console.log(token);
		if(token){
			setToken(token);
		}
		
	};
	function updateForm(value) {
		return setForm((prev) => {
			console.log(form);
			return { ...prev, ...value };
		});
	}
	useEffect(() => {
		if(isLoggedIn){
			navigate("/")
		}
	}, [isLoggedIn])
	
	return (
		<>
			<div className="container">
				<div className="row">
					<div className="col-md-12 min-vh-100 d-flex flex-column justify-content-center">
						<div className="row">
							<div className="col-lg-6 col-md-8 mx-auto">
								<div className="card rounded shadow shadow-sm">
									<div className="card-header">
										<h3 className="mb-0">Login</h3>
									</div>
									<div className="card-body">
										<form onSubmit={handleSubmit}>
											<div className="form-group">
												<label>
													Username
												</label>
												<input
													type="text"
													className="form-control form-control-lg rounded-0"
													required={true}
													onChange={(e) => updateForm({username:e.target.value})}
												/>
											</div>
											<div className="form-group mt-3">
												<label>Password</label>
												<input
													type="password"
													className="form-control form-control-lg rounded-0"
													required={true}
													onChange={(e) => updateForm({password:e.target.value})}
												/>
											</div>
											<button
												type="submit"
												className="btn btn-success btn-lg float-right mt-3"
											>
												Login
											</button>
										</form>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</>
	);
}

Login.propTypes = {
	setToken: PropTypes.func.isRequired,
};