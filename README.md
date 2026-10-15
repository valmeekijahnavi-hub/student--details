# Student Details & Academic Performance Dashboard

An interactive data-visualization project built with Python, Streamlit, Pandas, and Plotly.

## Dataset
Place `StudentPerformanceFactors.csv` in the same folder as `app.py`. This project is set up for the uploaded Student Performance Factors dataset.

## Features
- Sidebar filters for gender, school type, motivation, parental involvement, resources, internet access, and extracurricular activities.
- Range sliders for attendance, study hours, and exam scores.
- **All filters update every KPI and chart together.**
- KPI cards for student count, average score, median score, and average attendance.
- Exam-score histogram.
- Study hours vs. exam score scatter plot.
- Average exam score by motivation.
- Attendance vs. exam score scatter plot.
- Numeric correlation heatmap.
- Filtered data table and CSV download.

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Install the packages:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Start the app:

   ```bash
   python -m streamlit run app.py
   ```

5. Streamlit will show a local URL, usually `http://localhost:8501`.

## Upload to GitHub
1. Create a new repository on GitHub, for example `student-details-dashboard`.
2. Upload these files and folders:
   - `app.py`
   - `requirements.txt`
   - `README.md`
   - `StudentPerformanceFactors.csv`
3. Commit the files.

If using Git from the terminal:

   ```bash
   git init
   git add app.py requirements.txt README.md StudentPerformanceFactors.csv
   git commit -m "Add student details visualization dashboard"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/student-details-dashboard.git
   git push -u origin main
   ```

Replace `YOUR-USERNAME` with your GitHub username. If Git asks you to sign in, complete GitHub authentication.

## Deploy with Streamlit Community Cloud
1. Visit https://share.streamlit.io/
2. Sign in with GitHub and authorize access.
3. Choose **Create app**.
4. Select your repository, branch `main`, and main file path `app.py`.
5. Click **Deploy**.

## Important
The CSV contains student-related attributes. Use it only for your coursework and follow the dataset's Kaggle license/terms. Do not add personal student records without appropriate permission.
