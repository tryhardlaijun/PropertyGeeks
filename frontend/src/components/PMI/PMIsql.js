import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";

const Record = (props) => (
	<TableRow>
		<TableCell align="center">{props.record.street}</TableCell>
		<TableCell align="center">{props.record.project}</TableCell>
		<TableCell align="center">{props.record.propertyType}</TableCell>
		<TableCell align="center">
			{props.record.PRENT_ID ? "Rental" : "Sale"}
		</TableCell>
		<TableCell align="center">
			<button type="button" className="updatebutton me-1">
                    <Link
                    to={`/pmisaleSQl/${props.record.PMI_ID}`}
                    style={{ textDecoration: "none", color: "black" }}
                >
                    View
                </Link>
			</button>
		</TableCell>
	</TableRow>
);

function PMISQL() {
	const [PMIHouse, setPMIHouse] = useState([]);
	const [filter, setFilters] = useState({
		town: "",
		type: null,
	});
	const [types, setTypes] = useState([]);
	function handleOnchange(value) {
		console.log(value);
		return setFilters((prev) => {
			return { ...prev, ...value };
		});
	}

	useEffect(() => {
		async function getTypes() {
			try {
				const response = await axios(
					"http://127.0.0.1:5000/pmi/all/getPropertyType"	
				);
				console.log(response.data);
				const records = await response.data.Results;
				setTypes(records);
			} catch (error) {
				const message = `An error occurred: ${error}`;
				console.log(message);
				return;
			}
		}
		
		getTypes()

		return;
	}, []);

	function handleOnClick() {
		let URI = "http://127.0.0.1:5000/pmi/all/getPMIByFilter?";
		if (filter.town != null && filter.type != null) {
			URI = URI + `pid=${filter.type}&street=${filter.town}`;
			console.log(URI);
		} else if (filter.town != null) {
			URI = URI + `street=${filter.town}`;
			console.log(URI);
		} else if (filter.type != null) {
			URI = URI + `property_type=${filter.type}`;
			console.log(URI);
		}
		async function getRecords() {
			try {
				const response = await axios(URI);
				console.log(response.data);
				const records = await response.data.Results;
				setPMIHouse(records);
			} catch (error) {
				const message = `An error occurred: ${error}`;
				console.log(message);
				return;
			}
		}
		getRecords();
	}

	function recordList() {
		return PMIHouse.map((record, index) => {
			return <Record record={record} key={index} />;
		});
	}

	function typeList() {
		return types.map((type, index) => {
			return (
				<option key={type.FID} value={type.FID}>
					{type.room_type}
				</option>
			);
		});
	}

	return (
		<div className="container mt-3">
			<h2>PMI(SQL)</h2>
			<div className="row">
				<div className="col">
					<label className= "mx-1" htmlFor="project">
						Project:
					<input type="text" placeholder="Project Name" id="project" value={filter.town} onChange={(e) =>
							handleOnchange({ town: e.target.value })
						}>
					</input>
					</label>
				</div>
				<div className="col">
					<select
						class="form-control"
						onChange={(e) =>
							handleOnchange({ type: e.target.value })
						}
					>
						<option selected="true" disabled="disabled">
							Select Room Type
						</option>
						{typeList()}
					</select>
				</div>
				<div className="col">
					<button
						onClick={() => {
							handleOnClick();
						}}
						className="updatebuttonLong me-1">
						<b>Filter</b>
					</button>
				</div>
			</div>
			<TableContainer component={Paper}>
				<Table
					sx={{ minWidth: 300 }}
					size="large"
					aria-label="a dense table"
				>
					<TableHead>
						<TableRow style={{ background: "#E8DED1" }}>
							<TableCell align="center">
								<b>Street</b>
							</TableCell>
							<TableCell align="center">
								<b>Project Name</b>
							</TableCell>
							<TableCell align="center">
								<b>Proterty Type</b>
							</TableCell>
							<TableCell align="center">
								<b>Status</b>
							</TableCell>
							<TableCell align="center">
								<b>Actions</b>
							</TableCell>
						</TableRow>
					</TableHead>
					<TableBody>{recordList()}</TableBody>
				</Table>
			</TableContainer>
		</div>
	);
}

export default PMISQL;
