import { useEffect, useRef, useState } from "react";
import "./App.css";

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const fileInputRef = useRef(null);

  useEffect(() => {
    return () => {
      if (selectedImage) {
        URL.revokeObjectURL(selectedImage);
      }
    };
  }, [selectedImage]);

  const handleImageChange = (event) => {
    const file = event.target.files[0];

    if (!file) {
      return;
    }

    if (!file.type.startsWith("image/")) {
      setError("Please choose a valid image file.");
      setSelectedFile(null);
      setSelectedImage(null);
      setPrediction(null);
      event.target.value = "";
      return;
    }

    if (file) {
      setSelectedFile(file);
      setSelectedImage(URL.createObjectURL(file));
      setPrediction(null);
      setError("");
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setSelectedImage(null);
    setPrediction(null);
    setError("");

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handlePredict = async () => {
    if (!selectedFile) {
      setError("Please select an image first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    setLoading(true);
    setPrediction(null);
    setError("");

    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Prediction failed");
      }

      const data = await response.json();
      setPrediction(data);
    } catch (error) {
      console.error(error);
      setError("Could not connect to AI server. Please make sure FastAPI is running.");
    } finally {
      setLoading(false);
    }
  };

  const confidenceValue = prediction ? Math.max(0, Math.min(100, prediction.confidence)) : 0;

  return (
    <div className="app">

      {/* NAVBAR */}
      <nav className="navbar">
        <div className="logo">♻️ E-Waste AI</div>

        <div className="nav-links">
          <a href="#home">Home</a>
          <a href="#classify">Classify</a>
          <a href="#about">About</a>
        </div>
      </nav>

      {/* HOME */}
      <section className="hero" id="home">

        <div className="hero-content">

          <p className="tag">
            AI-POWERED E-WASTE MANAGEMENT
          </p>

          <h1>
            Identify E-Waste.
            <br />
            <span>Recycle Responsibly.</span>
          </h1>

          <p className="description">
            Upload an electronic waste image and our AI model will
            identify the item and provide a suitable recycling recommendation.
          </p>

          <button
            className="primary-btn"
            onClick={() =>
              document
                .getElementById("classify")
                .scrollIntoView({ behavior: "smooth" })
            }
          >
            ♻️ Classify E-Waste
          </button>

        </div>

        <div className="hero-card">

          <div className="circle">♻️</div>

          <h2>Smart Recycling</h2>

          <p>
            AI-powered classification for responsible e-waste management.
          </p>

        </div>

      </section>

      {/* CLASSIFICATION */}
      <section className="classify-section" id="classify">

        <p className="tag">
          AI CLASSIFICATION
        </p>

        <h2>
          Classify Your E-Waste
        </h2>

        <p>
          Upload an image to identify the type of electronic waste.
        </p>

        <div className="upload-box">

          <div className="upload-icon">
            📷
          </div>

          <h3>
            Upload an E-Waste Image
          </h3>

          <p>
            Select an image of your electronic waste
          </p>

          <label className="upload-btn">
            Choose Image

            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              hidden
            />

          </label>

          {/* IMAGE PREVIEW */}
          {selectedImage && (
            <div className="image-preview">

              <h3>Selected Image</h3>

              <img
                src={selectedImage}
                alt="Selected e-waste"
              />

              <button
                className="predict-btn"
                onClick={handlePredict}
                disabled={loading}
              >
                {loading ? "🔄 Analyzing..." : "🤖 Predict E-Waste"}
              </button>

              <button
                className="secondary-btn"
                onClick={handleReset}
                type="button"
              >
                Choose Another Image
              </button>

            </div>
          )}

          {error && (
            <div className="error-message" role="alert">
              {error}
            </div>
          )}

          {/* PREDICTION RESULT */}
          {prediction && (
            <div className={`prediction-result ${prediction.is_low_confidence ? "low-confidence" : ""}`}>

              <h2>
                {prediction.is_low_confidence
                  ? "Prediction Needs Review"
                  : "♻️ Prediction Result"}
              </h2>

              {!prediction.is_low_confidence && (
                <h3>
                  {prediction.prediction}
                </h3>
              )}

              <p>
                Confidence: {prediction.confidence}%
              </p>

              <div className="confidence-meter" aria-hidden="true">
                <div
                  className={`confidence-fill ${prediction.is_low_confidence ? "low" : "high"}`}
                  style={{ width: `${confidenceValue}%` }}
                />
              </div>

              <p className="confidence-note">
                {prediction.is_low_confidence
                  ? "Confidence is below the 70% review threshold. Please try a clearer image."
                  : "Confidence is above the 70% recommendation threshold."}
              </p>

              {prediction.is_low_confidence ? (
                <p className="prediction-warning">
                  {prediction.message}
                </p>
              ) : (
                <div className="recommendation-card">
                  <h4>Recycling Recommendation</h4>

                  <p>
                    {prediction.recommendation}
                  </p>
                </div>
              )}

            </div>
          )}

        </div>

      </section>

      {/* ABOUT */}
      <section className="about-section" id="about">

        <p className="tag">
          ABOUT THE PROJECT
        </p>

        <h2>
          Why E-Waste Management Matters
        </h2>

        <p>
          Electronic waste contains valuable materials but can also
          create environmental problems when improperly disposed of.
          This project uses Artificial Intelligence to support better
          identification, segregation, and responsible recycling.
        </p>

        <div className="features">

          <div className="feature-card">
            <div>🤖</div>

            <h3>
              AI Classification
            </h3>

            <p>
              Identifies different types of electronic waste.
            </p>
          </div>

          <div className="feature-card">
            <div>♻️</div>

            <h3>
              Recycling Guidance
            </h3>

            <p>
              Provides suitable recycling recommendations.
            </p>
          </div>

          <div className="feature-card">
            <div>🌱</div>

            <h3>
              Environmental Impact
            </h3>

            <p>
              Supports responsible e-waste management.
            </p>
          </div>

        </div>

      </section>

      {/* FOOTER */}
      <footer>
        <p>
          ♻️ AI-Based E-Waste Classification & Recycling Recommendation
        </p>
      </footer>

    </div>
  );
}

export default App;