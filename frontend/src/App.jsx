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
				`${import.meta.env.VITE_API_URL}/api/optimize-order/`,
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
						<h3>Calculation Result</h3>

						<p>
							<strong>Raw Tubes Required:</strong>{" "}
							{result.raw_tubes_required}
						</p>

						<h4 className="section-title">Vendor Comparison</h4>

						{result.vendors.map((vendor) => (
							<div
								key={vendor.name}
								className={`vendor-card ${
									vendor.is_best ? "best-vendor" : ""
								}`}
							>
								<div className="vendor-header">
									<strong>{vendor.name}</strong>
									{vendor.is_best && (
										<span className="badge">
											Best Option
										</span>
									)}
								</div>

								<p>Total Cost: ₹{vendor.total_cost}</p>
								<p>
									Delivery Time: {vendor.delivery_days} days
								</p>
							</div>
						))}
					</div>
				)}
			</div>
		</div>
	);
}

export default App;
