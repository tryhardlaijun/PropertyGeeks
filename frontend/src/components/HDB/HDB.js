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
			<button type="button" className="updatebutton me-1">
				<Link
					to={`/resale/${props.record.FD_ID}`}
					style={{ textDecoration: "none", color: "black" }}
				>
					View
				</Link>
			</button>
		</TableCell>
	</TableRow>
);

function HDB() {
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
		let URI = "http://127.0.0.1:5000/flat/all/getFlatsByFilter?";
		if (filter.town != null && filter.type != null) {
			URI = URI + `fid=${filter.type}&rid=${filter.town}`;
			console.log(URI);
		} else if (filter.town != null) {
			URI = URI + `rid=${filter.town}`;
			console.log(URI);
		} else if (filter.type != null) {
			URI = URI + `fid=${filter.type}`;
			console.log(URI);
		}
		async function getRecords() {
			try {
				const response = await axios(URI);
				console.log(response.data);
				const records = await response.data.Results;
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
					"http://127.0.0.1:5000/flat/all/getFlatTypes"
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
		async function getRegion() {
			try {
				const response = await axios(
					"http://127.0.0.1:5000/flat/all/getRegion"
				);
				console.log(response.data);
				const records = await response.data.Results;
				setTowns(records);
			} catch (error) {
				const message = `An error occurred: ${error}`;
				console.log(message);
				return;
			}
		}
		if (filter.town === null && filter.type === null) {
			getRegion().then(() => {
				getTypes();
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
				<option key={town.RID} value={town.RID}>
					{town.town}
				</option>
			);
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

export default HDB;
