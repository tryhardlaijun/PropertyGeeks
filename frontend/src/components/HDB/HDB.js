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
				<Link to={`/resale/${props.record.FD_ID}`} style={{ textDecoration: "none", color: "black" }}>
					View 
				</Link>
			</button>
		</TableCell>
	</TableRow>
);

function HDB() {
	const [HDBFlats, setHDBFlats] = useState([]);
    const [filter, setFilters] = useState({})
	useEffect(() => {
		async function getRecords() {
			try {
				const response = await axios(
					"http://127.0.0.1:5000/flat/all/getFlatsByFilter"
				);
				console.log(response.data);
				const records = await response.data.Results;
				setHDBFlats(records);
			} catch (error) {
				const message = `An error occurred: ${error}`;
				window.alert(message);
				return;
			}
		}
		getRecords();

		return;
	}, []);

	function recordList() {
		return HDBFlats.map((record, index) => {
			return <Record record={record} key={index} />;
		});
	}

	return (
		<div className="container mt-3">
			<h2>HDB</h2>
            <div className="row">
                <div className="col">Town</div>
                <div className="col">Block</div>
                <div className="col">Room-type</div>
                <div className="col">Price</div>
                <div className="col">Year</div>
                <div className="col">Model</div>
            </div>
			<TableContainer component={Paper}>
				<Table
					sx={{ minWidth: 300 }}
					size="large"
					aria-label="a dense table"
				>
					<TableHead>
						<TableRow style={{ background: "#E8DED1" }}>
							<TableCell align="center"><b>Town</b></TableCell>
							<TableCell align="center"><b>Block</b></TableCell>
							<TableCell align="center"><b>Room-Type</b></TableCell>
							<TableCell align="center"><b>Size (sqm)</b></TableCell>
							<TableCell align="center"><b>Actions</b></TableCell>
						</TableRow>
					</TableHead>
					<TableBody>{recordList()}</TableBody>
				</Table>
			</TableContainer>
		</div>
	);
}

export default HDB;