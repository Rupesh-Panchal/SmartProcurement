import { useState } from "react";
import "./App.css";

function App() {
	const [requiredLength, setRequiredLength] = useState("");
	const [quantity, setQuantity] = useState("");
	const [result, setResult] = useState(null);
	const [error, setError] = useState("");
	const [loading, setLoading] = useState(false);

	const handleSubmit = async (e) => {
		e.preventDefault();
		setError("");
		setResult(null);
		setLoading(true);

		try {
			const response = await fetch(
				"http://127.0.0.1:8000/api/optimize-order/",
				{
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({
						required_length: Number(requiredLength),
						quantity: Number(quantity),
					}),
				},
			);

			const data = await response.json();

			if (!response.ok) {
				throw new Error("Something went wrong");
			}

			setResult(data);
		} catch (err) {
			setError("Failed to fetch data from backend");
		} finally {
			setLoading(false);
		}
	};

	return (
		<div className="app-container">
			<div className="card">
				<h2>Smart Procurement</h2>

				<form onSubmit={handleSubmit}>
					<div className="form-group">
						<label>Required Length (mm)</label>
						<input
							type="number"
							value={requiredLength}
							onChange={(e) => setRequiredLength(e.target.value)}
							required
						/>
					</div>

					<div className="form-group">
						<label>Quantity</label>
						<input
							type="number"
							value={quantity}
							onChange={(e) => setQuantity(e.target.value)}
							required
						/>
					</div>

					<button type="submit" disabled={loading}>
						{loading ? "Optimizing..." : "Optimize Order"}
					</button>
				</form>

				{error && <p className="error">{error}</p>}

				{result && (
					<div className="result-card">
						<h3>Result</h3>
						<p>
							<strong>Raw Tubes Required:</strong>{" "}
							{result.raw_tubes_required}
						</p>
						<p>
							<strong>Vendor:</strong> {result.vendor.name}
						</p>
						<p>
							<strong>Total Cost:</strong> ₹
							{result.vendor.total_cost}
						</p>
						<p>
							<strong>Delivery Time:</strong>{" "}
							{result.vendor.delivery_days} days
						</p>
					</div>
				)}
			</div>
		</div>
	);
}

export default App;
