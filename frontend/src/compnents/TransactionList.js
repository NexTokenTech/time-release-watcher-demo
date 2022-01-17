import "./TransactionList.scss"
import React from "react"
import axios from "axios"

function TransactionList(props){
	console.log(props);
	function transactionBtnPressed() {
		console.log("transactionBtnPressed");
	}
	return (
		<div>
			<div>
				<div>This is Page1!</div>
			</div>
			
		</div>
	);
}
export default TransactionList;