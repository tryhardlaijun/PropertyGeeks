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
		<TableCell align="center">{props.record.town}</TableCell>
		<TableCell align="center">{props.record.block}</TableCell>
		<TableCell align="center">{props.record.room_type}</TableCell>
		<TableCell align="center">{props.record.floor_area_sqm}</TableCell>
		<TableCell align="center">
			{props.record.PRENT_ID ? "Rental" : "Sale"}
		</TableCell>
		<TableCell align="center">
			<button type="button" className="updatebutton me-1">
				{props.record.RT_ID ? (
					<Link to={`/HDBNOSQLRent/${props.record.RT_ID}`} style={{ textDecoration: "none", color: "black" }}>
						View
					</Link>
				) : (
                    <Link
                    to={`/HDBNOSQLSale/${props.record.RS_ID}`}
                    style={{ textDecoration: "none", color: "black" }}
                >
                    View
                </Link>
				)}
			</button>
		</TableCell>
	</TableRow>
);

function HDBNOSQL() {
	const [HDBFlats, setHDBFlats] = useState([]);
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
		let URI = "http://127.0.0.1:5001/flat/all/getFlatsByFilter?";
		if (filter.town != null && filter.type != null) {
			URI = URI + `flat_type=${filter.type}&region=${filter.town}`;
			console.log(URI);
		} else if (filter.town != null) {
			URI = URI + `region=${filter.town}`;
			console.log(URI);
		} else if (filter.type != null) {
			URI = URI + `flat_type=${filter.type}`;
			console.log(URI);
		}
		async function getRecords() {
			try {
				const response = await axios(URI);
				console.log(response.data);
				const records = await response.data;
				setHDBFlats(records);
			} catch (error) {
				const message = `An error occurred: ${error}`;
				console.log(message);
				return;
			}
		}
		async function getTypes() {
			try {
				const response = await axios(
					"http://127.0.0.1:5001/flat/all/getFlatTypes"
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
					"http://127.0.0.1:5001/flat/all/getRegion"
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
		if (filter.town === null && filter.type === null) {
			getTypes().then(() =>
				getRegion().then(() => {
				})
				.catch((error)=>{
					console.log(error);
				})
			).catch((error)=>{
				console.log(error);
			});
		} else {
			getRecords();
		}
		return;
	}, [filter.town, filter.type]);

	function recordList() {
		return HDBFlats.map((record, index) => {
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
			<h2>HDB</h2>
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
								<b>Town</b>
							</TableCell>
							<TableCell align="center">
								<b>Block</b>
							</TableCell>
							<TableCell align="center">
								<b>Room-Type</b>
							</TableCell>
							<TableCell align="center">
								<b>Size (sqm)</b>
							</TableCell>
							<TableCell align="center">
								<b>Rental/Sale</b>
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

export default HDBNOSQL;
