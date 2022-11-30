import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
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
		<TableCell align="center">{props.record.PMI_ID ? ("Private Property"
				) : ("HDB"
				)}</TableCell>
                <TableCell align="center">{props.record.PMI_ID ? (props.record.project
				) : ("Block " + props.record.block + `(${props.record.model})`
				)}</TableCell>
		<TableCell align="center">{props.record.Description}</TableCell>
		<TableCell align="center">
			<button type="button" className="updatebutton me-1">
				{props.record.PMI_ID ? (
					<Link
						to={`/pmisaleSQl/${props.record.PMI_ID}`}
						style={{ textDecoration: "none", color: "black" }}
					>
						View
					</Link>
				) : (
					<Link
						to={`/resale/${props.record.FD_ID}`}
						style={{ textDecoration: "none", color: "black" }}
					>
						View
					</Link>
				)}
			</button>
			<button type="button" className="updatebutton me-1">
			<Link
						to={`/updateBM/${props.record.BookmarkID}/${props.uid}`}
						style={{ textDecoration: "none", color: "black" }}
					>
						Update this
					</Link>
			</button>
			<button type="button" className="updatebutton me-1">
			<Link
						to={`/delBM/${props.record.BookmarkID}/${props.uid}`}
						style={{ textDecoration: "none", color: "black" }}
					>
						Delete
					</Link>
			</button>
		</TableCell>
	</TableRow>
);

function Bookmark() {
	const navigate = useNavigate();
	const [bookmarks, setBookMarks] = useState([]);
	useEffect(() => {
		const tokenString = localStorage.getItem('token');
		const userToken = JSON.parse(tokenString);
		console.log(userToken);
		var bodyFormData = new FormData();
		bodyFormData.append("UserID", 3);
		if(!userToken){
			window.alert("Please Login")
			navigate("/")
		}
		let URI = "http://127.0.0.1:5000/view/getBookmark";
		async function getRecords() {
			console.log(bodyFormData)
			try {
				const response = await axios({
					method: "post",
					url: URI,
					data: bodyFormData,
					headers: { "Content-Type": "multipart/form-data" },
				});
				console.log(response.data);
				setBookMarks(response.data.Results);
			} catch (error) {
				const message = `An error occurred: ${error}`;
				console.log(message);
				return;
			}
		}
		getRecords().then(()=>{
			console.log("done");
		}).catch((error)=>{
			console.log(error);
		});
		return;
	}, []);

	function recordList() {
		return bookmarks.map((record, index) => {
			return <Record record={record} key={index} uid = {3}/>;
		});
	}
	return (
		<div className="container mt-3">
			<h2>Bookmarks</h2>
			<TableContainer component={Paper}>
				<Table
					sx={{ minWidth: 300 }}
					size="large"
					aria-label="a dense table"
				>
					<TableHead>
						<TableRow style={{ background: "#E8DED1" }}>
							<TableCell align="center">
								<b>Type</b>
							</TableCell>
                            <TableCell align="center">
								<b>Details</b>
							</TableCell>
							<TableCell align="center">
								<b>Description</b>
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

export default Bookmark;
