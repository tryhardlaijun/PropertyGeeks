import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";
import BookmarkIcon from "@mui/icons-material/Bookmark";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";

function SaleNoSql() {
	const params = useParams();
	console.log(params.id);
	const [houseDetails, setHouseDetails] = useState({});
	const [housePrice, setHousePrice] = useState([])
	useEffect(() => {
		async function getSalePrice() {
			const response = await axios(
				`http://127.0.0.1:5001/flat/filter/getFlatPrice?resale_id=${params.id}`
			);
			const price = await response.data;
			console.log(price);
			setHousePrice(price);
			setHouseDetails(price[0])
			console.log(houseDetails);
			return;
		}
		async function getFlatDetail() {
			const response = await axios(
				`http://127.0.0.1:5001/flat/filter/getResaleFlatDetails?resale_id=${params.id}`
			);
			const price = await response.data;
			console.log(price);
			setHousePrice(price);
			setHouseDetails(price[0])
			console.log(houseDetails);
			return;
		}
		getSalePrice().then(()=>{
			getFlatDetail()
		})
	}, []);

	const Record = (props) => (
		<TableRow>
			<TableCell align="center">
				<p className="bodyText">{props.record.quarter}</p>
			</TableCell>
			<TableCell align="center">
				<p className="bodyText">{props.record.year}</p>
			</TableCell>
			<TableCell align="center">
				<p className="bodyText">${props.record.price}</p>
			</TableCell>
		</TableRow>
	);

	function recordList() {
		return housePrice.map((record, index) => {
			return <Record record={record} key={index} />;
		});
	}

	function displayHeader() {
		return (
			<h1 className="headingFont">
				Block {houseDetails.block} {houseDetails.town}
			</h1>
		);
	}

	function displayDetails() {
		return (
			<div className="card">
				<div className="card-header">
					<h4 className="text-center headingFont">HDB Details</h4>
				</div>
				<div className="card-body">
					<table class="table table-striped text-center">
						<tbody>
							<tr>
								<td>
									<p className="bodyText">
										<b>Block</b>
									</p>
								</td>
								<td>
									<p className="bodyText">
										<b>Town</b>
									</p>
								</td>
							</tr>
							<tr>
								<td>
									<p className="bodyText">
										{houseDetails.block}
									</p>
								</td>
								<td>
									<p className="bodyText">
										{houseDetails.town}
									</p>
								</td>
							</tr>
						</tbody>
						<tbody>
							<tr>
								<td>
									<p className="bodyText">
										<b>Year of Lease Start</b>
									</p>
								</td>
								<td>
									<p className="bodyText">
										<b>Room Type</b>
									</p>
								</td>
							</tr>
							<tr>
								<td>
									<p className="bodyText">
										{houseDetails.lease_commence_date}
									</p>
								</td>
								<td>
									<p className="bodyText">
										{houseDetails.room_type}
									</p>
								</td>
							</tr>
						</tbody>
						<tbody>
							<tr>
								<td>
									<p className="bodyText">
										<b>Size</b>
									</p>
								</td>
								<td>
									<p className="bodyText">
										<b>Model</b>
									</p>
								</td>
							</tr>
							<tr>
								<td>
									<p className="bodyText">
										{houseDetails.floor_area_sqm} sqm
									</p>
								</td>
								<td>
									<p className="bodyText">
										{houseDetails.model}
									</p>
								</td>
							</tr>
						</tbody>
					</table>
					<button type="button" className="updatebuttonLong me-1">
						<Link
							style={{ textDecoration: "none", color: "black" }}
						>
							Add to Bookmark <BookmarkIcon />
						</Link>
					</button>
				</div>
			</div>
		);
	}

	function displayPrice() {
		return (
			<div className="card">
				<div className="card-header">
					<h4 className="text-center headingFont">Resale Price History</h4>
				</div>
				<div className="card-body">
					<TableContainer component={Paper}>
						<Table
							sx={{ minWidth: 300 }}
							size="large"
							aria-label="a dense table"
						>
							<TableHead>
								<TableRow style={{ background: "#E8DED1" }}>
									<TableCell align="center">
										<b>Quarter</b>
									</TableCell>
									<TableCell align="center">
										<b>Year</b>
									</TableCell>
									<TableCell align="center">
										<b>Price</b>
									</TableCell>
								</TableRow>
							</TableHead>
							<TableBody>{recordList()}</TableBody>
						</Table>
					</TableContainer>
				</div>
			</div>
		);
	}

	return (
		<div className="container mt-3">
			{displayHeader()}
			<div className="row">
				<div className="col-4 border">{displayDetails()}</div>
				<div className="col-8 border">{displayPrice()}</div>
			</div>
		</div>
	);
}
export default SaleNoSql;
