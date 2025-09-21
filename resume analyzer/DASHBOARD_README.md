# Resume Analyzer Dashboard

A comprehensive Streamlit-based dashboard for analyzing resumes with ATS (Applicant Tracking System) compatibility scoring and detailed improvement recommendations.

## Features

### 🎯 ATS Analysis
- **ATS Compatibility Score** - Comprehensive scoring system that evaluates how well your resume will perform in ATS systems
- **Keyword Optimization** - Analyzes keyword density and relevance for technical, soft skills, and industry-specific terms
- **Format Compliance** - Checks resume format against ATS requirements
- **Red Flag Detection** - Identifies elements that may hurt ATS performance

### 📊 Comprehensive Scoring
- **Overall Resume Score** - Weighted average of all components
- **Component Scores** - Individual scores for skills, experience, education, and format
- **Detailed Metrics** - In-depth analysis of each resume section

### 📈 Visualizations
- **Interactive Charts** - Plotly-powered visualizations for scores and metrics
- **Skills Distribution** - Pie charts showing technical vs soft skills
- **Keyword Analysis** - Bar charts and tables for keyword density
- **Score Breakdowns** - Horizontal bar charts for component scores

### 💡 Smart Recommendations
- **General Recommendations** - Based on resume best practices
- **ATS-Specific Tips** - Targeted advice for ATS optimization
- **Missing Elements** - Identifies what's missing from your resume
- **Improvement Suggestions** - Actionable steps to enhance your resume

## Getting Started

### Prerequisites
- Python 3.7+
- All dependencies from `requirements.txt`

### Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the dashboard:
   ```bash
   streamlit run dashboard.py
   ```

3. Open your browser to `http://localhost:8501`

### Usage

1. **Upload Resume**: Use the file uploader in the sidebar to upload your resume
2. **Configure Options**: Choose which analyses to include
3. **Review Results**: Navigate through the different tabs to see comprehensive analysis
4. **Implement Recommendations**: Follow the suggested improvements to optimize your resume

## Supported File Formats

- **PDF** (.pdf) - Most common format for resumes
- **Microsoft Word** (.docx, .doc) - Widely used document format
- **Plain Text** (.txt) - Simple text format
- **Rich Text Format** (.rtf) - Formatted text documents

## Dashboard Sections

### 📊 Overview Tab
- Personal information summary
- Overall and ATS scores with color coding
- Quick statistics and metrics

### 🎯 ATS Analysis Tab
- Detailed ATS compatibility scoring
- Format compliance checks
- Red flags and missing elements
- Component score breakdowns

### 📝 Content Analysis Tab
- Skills categorization and analysis
- Work experience detailed review
- Education background analysis
- Content quality assessment

### 💡 Recommendations Tab
- General improvement suggestions
- ATS-specific optimization tips
- Prioritized action items

### 📈 Detailed Metrics Tab
- Keyword density analysis
- Skills distribution charts
- Text statistics and readability metrics
- Interactive visualizations

## ATS Scoring System

The ATS analyzer evaluates resumes on five key components:

1. **Keyword Optimization (25%)** - Relevance and density of industry keywords
2. **Format Compliance (20%)** - File format, length, and structure adherence
3. **Structure (20%)** - Organization, section headers, and chronological order
4. **Content Quality (20%)** - Quantified achievements and action verbs
5. **Completeness (15%)** - Essential information and section completeness

## Tips for Better ATS Performance

- Use standard section headers (Experience, Education, Skills)
- Include relevant keywords from job descriptions
- Quantify achievements with specific numbers and percentages
- Use bullet points for better readability
- Keep resume length between 300-700 words
- Avoid graphics, tables, or complex formatting
- Use standard fonts (Arial, Calibri, Times New Roman)
- Save as PDF or DOCX format

## Technical Details

### Architecture
- **Frontend**: Streamlit with custom CSS styling
- **Backend**: Python with modular resume analysis components
- **Visualizations**: Plotly for interactive charts and graphs
- **File Processing**: Multi-format parser system (PDF, DOCX, TXT, RTF)

### Key Components
- `dashboard.py` - Main Streamlit application
- `ats_analyzer.py` - Comprehensive ATS analysis engine
- `scoring.py` - Resume scoring algorithms
- `parsers/` - File format parsers
- `analyzers/` - Content analysis modules
- `models/` - Data models and structures

## Troubleshooting

### Common Issues
1. **File Upload Errors**: Ensure file is in supported format and not corrupted
2. **Analysis Failures**: Check that all dependencies are installed correctly
3. **Display Issues**: Clear browser cache and refresh the page

### Performance
- Large files may take longer to process
- Complex resumes with many sections may require more analysis time
- Visualizations are generated on-demand for better performance

## Contributing

To contribute to the dashboard:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.
