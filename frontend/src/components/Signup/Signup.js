import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function Signup() {
	var navigate = useNavigate()
	const [form, setForm] = useState({
		email: "",
		password: "",
		phoneNumber: "",
		cfPassword: "",
		address: "",
	});

	function updateForm(value) {
		return setForm((prev) => {
			console.log(form);
			return { ...prev, ...value };
		});
	}

	async function onSubmit(e){
		const newPerson = {...form}
		await fetch("http://127.0.0.1:5000/registerAPI",{
			method:"POST",
			headers:{
				"Content-Type": "application/json"
			},
			body:JSON.stringify(newPerson)
		}).then((res)=>{
			console.log(res);
			navigate("/login")
		})
		.catch(error => {
			window.alert(error);
			return
		})
		console.log(form);
	}

	return (
		<div className="parentForm mt-3">
			<div className="card">
				<div className="card-header text-center">Sign Up</div>
				<div className="card-body">
					
					<div className="mb-3">
						<label
							htmlFor="exampleFormControlInput1"
							className="form-label"
						>
							Email address
						</label>
						<input
							type="email"
							className="form-control"
							placeholder="name@example.com"
							value = {form.email}
							onChange={(e)=>{updateForm({email:e.target.value})}}
						/>
					</div>
					<div className="mb-3">
						<label
							htmlFor="exampleFormControlInput1"
							className="form-label"
						>
							Password
						</label>
						<input
							type="password"
							className="form-control"
							placeholder="Password"
							value = {form.password}
							onChange={(e)=>{updateForm({password:e.target.value})}}
						/>
					</div>
					<div className="mb-3">
						<label
							htmlFor="exampleFormControlInput1"
							className="form-label"
						>
							Confirm Password
						</label>
						<input
							type="password"
							className="form-control"
							placeholder="Confirm Password"
							value = {form.cfPassword}
							onChange={(e)=>{updateForm({cfPassword:e.target.value})}}
						/>
					</div>
					<div className="mb-3">
						<label
							htmlFor="exampleFormControlInput1"
							className="form-label"
						>
							Address
						</label>
						<input
							type="text"
							className="form-control"
							placeholder="Address"
							value={form.address}
							onChange={(e)=>{updateForm({address:e.target.value})}}
						/>
					</div>
					<div className="mb-3">
						<label
							htmlFor="exampleFormControlInput1"
							className="form-label"
						>
							Phone Number
						</label>
						<input
							type="text"
							className="form-control"
							placeholder="Phone Number"
							value={form.phoneNumber}
							onChange={(e)=>{updateForm({phoneNumber:e.target.value})}}
						/>
					</div>
					<button className="updatebuttonLong" type="submit" onClick={onSubmit}>Sign Up</button>
					
				</div>
			</div>
		</div>
	);
}

export default Signup;
