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
				{props.record.PRENT_ID ? (
					<Link to={`/pmirental/${props.record.PRENT_ID}`} style={{ textDecoration: "none", color: "black" }}>
						View
					</Link>
				) : (
                    <Link
                    to={`/pmisale/${props.record.PSALE_ID}`}
                    style={{ textDecoration: "none", color: "black" }}
                >
                    View
                </Link>
				)}
			</button>
		</TableCell>
	</TableRow>
);

function PMI() {
	const [PMIHouse, setPMIHouse] = useState([]);
	const [filter, setFilters] = useState({
		town: null,
		type: null,
	});
	const [types, setTypes] = useState([]);
	const [towns, setTowns] = useState([]);
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
					"http://127.0.0.1:5001/pmi/all/getPropertyType"
				);
				console.log(response.data);
				const records = await response.data;
				setTypes(records);
			} catch (error) {
				const message = `An error occurred: ${error}`;
				console.log(message);
				return;
			}
		}
		async function getRegion() {
			try {
				const response = await axios(
					"http://127.0.0.1:5001/pmi/all/getStreets"
				);
				console.log(response.data);
				const records = await response.data;
				setTowns(records);
			} catch (error) {
				const message = `An error occurred: ${error}`;
				console.log(message);
				return;
			}
		}
		getRegion().then(() => {
			getTypes().then(() => {
			});
		});

		return;
	}, []);

	function handleOnClick() {
		let URI = "http://127.0.0.1:5001/pmi/all/getPMIByFilter?";
		if (filter.town != null && filter.type != null) {
			URI = URI + `property_type=${filter.type}&street=${filter.town}`;
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
				const records = await response.data;
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

	function townList() {
		return towns.map((town, index) => {
			return (
				<option key={index} value={town._id}>
					{town._id}
				</option>
			);
		});
	}

	function typeList() {
		return types.map((type, index) => {
			return (
				<option key={index} value={type._id}>
					{type._id}
				</option>
			);
		});
	}

	return (
		<div className="container mt-3">
			<h2>PMI(NOSQL)</h2>
			<div className="row">
				<div className="col">
					<select
						class="form-control"
						onChange={(e) =>
							handleOnchange({ town: e.target.value })
						}
					>
						<option selected="true" disabled="disabled">
							Select Town
						</option>
						{townList()}
					</select>
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

export default PMI;
