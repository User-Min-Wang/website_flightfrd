<template>

  <div class="about-page">
    <div class="about-container">
      <h1>About FlightFRD</h1>
      
      <section class="about-section">
        <h2>Our Mission</h2>
        <p>
          FlightFRD is a comprehensive aircraft tracking and air traffic control monitoring platform. 
          We provide real-time data on aircraft movements, ATC communications, and flight information 
          to aviation enthusiasts, professionals, and researchers.
        </p>
      </section>
      
      <section class="about-section">
        <h2>Features</h2>
        <ul class="features-list">
          <li>
            <strong>Live Aircraft Tracking</strong>
            <p>Monitor aircraft positions in real-time with detailed flight information</p>
          </li>
          <li>
            <strong>ATC Communications</strong>
            <p>Access air traffic control message logs and communications</p>
          </li>
          <li>
            <strong>Flight Calendar</strong>
            <p>View scheduled flights and historical flight data</p>
          </li>
          <li>
            <strong>Aircraft Database</strong>
            <p>Browse detailed information about various aircraft types</p>
          </li>
        </ul>
      </section>
      
      <section class="about-section">
        <h2>Data Sources</h2>
        <p>
          Our platform aggregates data from multiple sources including:
        </p>
        <ul>
          <li>OpenSky Network API for ADS-B aircraft position data</li>
          <li>Public ATC communication feeds</li>
          <li>User-contributed flight information and images</li>
        </ul>
      </section>
      
      <section class="about-section">
        <h2>Contact Us</h2>
        <p>
          Have questions or suggestions? Reach out to us at:
          <a href="mailto:info@flightfrd.com">info@flightfrd.com</a>
        </p>
      </section>
    </div>

  </div>
</template>

<script setup lang="ts">

// About page component
</script>

<style scoped>
.about-page {
  padding: 40px 20px;
  background-color: #f5f6fa;
  min-height: calc(100vh - 120px);
}

.about-container {
  max-width: 900px;
  margin: 0 auto;
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.about-container h1 {
  color: #2c3e50;
  margin-bottom: 30px;
  text-align: center;
  font-size: 2.5rem;
}

.about-section {
  margin-bottom: 40px;
}

.about-section h2 {
  color: #34495e;
  margin-bottom: 15px;
  font-size: 1.5rem;
  border-bottom: 2px solid #3498db;
  padding-bottom: 10px;
}

.about-section p {
  color: #555;
  line-height: 1.8;
  margin-bottom: 15px;
}

.features-list {
  list-style: none;
  padding: 0;
}

.features-list li {
  margin-bottom: 20px;
  padding-left: 20px;
  border-left: 3px solid #3498db;
}

.features-list strong {
  display: block;
  color: #2c3e50;
  font-size: 1.1rem;
  margin-bottom: 5px;
}

.features-list p {
  margin: 0;
  color: #666;
}

.about-section ul {
  color: #555;
  line-height: 1.8;
  padding-left: 20px;
}

.about-section a {
  color: #3498db;
  text-decoration: none;
}

.about-section a:hover {
  text-decoration: underline;
}
</style>
