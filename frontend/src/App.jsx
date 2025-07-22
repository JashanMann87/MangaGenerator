import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [prompt, setPrompt] = useState('');
  const [imageUrl, setImageUrl] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setImageUrl(''); // Clear previous image

    try {
      // Make a POST request to our backend API
      const response = await axios.post(
        'http://127.0.0.1:8000/api/v1/generate-image',
        { prompt: prompt },
        { responseType: 'blob' } // Important: we expect an image blob back
      );

      // Create a URL from the returned blob
      const localUrl = URL.createObjectURL(response.data);
      setImageUrl(localUrl);

    } catch (error) {
      console.error("Error generating image:", error);
      alert("Failed to generate image. Check the console for details.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>StoryWeaver AI 🎨</h1>
        <p>Enter a prompt to generate a panel for your story.</p>
      </header>
      <main>
        <form onSubmit={handleSubmit} className="prompt-form">
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="e.g., a warrior princess in a neon-lit city"
            required
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Generating...' : 'Generate'}
          </button>
        </form>

        <div className="image-container">
          {loading && <div className="spinner"></div>}
          {imageUrl && !loading && (
            <img src={imageUrl} alt="Generated art" />
          )}
        </div>
      </main>
    </div>
  );
}

export default App;