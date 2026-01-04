import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Health Data Quality Guardian",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS styling
st.markdown("""
    <style>
    .main {
        background: linear-gradient(to bottom right, #EFF6FF, #E0E7FF);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: white;
        border-radius: 8px;
        padding: 0 24px;
        font-weight: 600;
        color: #374151;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2563EB !important;
        color: white !important;
    }
    div[data-testid="stExpander"] {
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    div[data-testid="stExpander"]:hover {
        box-shadow: 0 10px 15px rgba(0, 0, 0, 0.15);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_anomaly' not in st.session_state:
    st.session_state.selected_anomaly = None

# Data definitions
dashboard_stats = {
    'total_records': 45821,
    'critical_issues': 23,
    'warning_issues': 47,
    'clean_records': 45751,
    'quality_score': 97.8
}

anomalies = [
    {
        'id': 1,
        'type': 'Critical',
        'category': 'Missing Second Dose',
        'count': 12,
        'description': 'Patients overdue for second dose by >30 days',
        'impact': 'High - Incomplete vaccination coverage',
        'ai_explanation': 'These 12 patients received their first dose but are significantly overdue for the second dose. Analysis shows 8 were due to follow-up failures, 3 to address changes, and 1 to data entry error.',
        'recommendation': 'Immediate outreach required. Priority contact list generated.'
    },
    {
        'id': 2,
        'type': 'Critical',
        'category': 'Age Mismatch',
        'count': 8,
        'description': 'Vaccination age conflicts with birth records',
        'impact': 'High - Data integrity issue',
        'ai_explanation': 'Detected inconsistencies between vaccination dates and ages. 5 cases show impossible timelines (vaccination before birth), 3 cases have data entry errors in birth year.',
        'recommendation': 'Manual review required. Likely data entry errors in patient ID or DOB fields.'
    },
    {
        'id': 3,
        'type': 'Warning',
        'category': 'Duplicate Records',
        'count': 15,
        'description': 'Potential duplicate patient entries',
        'impact': 'Medium - Inflated coverage statistics',
        'ai_explanation': 'Found 15 patient records with matching names and similar DOBs across different IDs. Pattern suggests potential duplicate registrations during high-volume vaccination events.',
        'recommendation': 'De-duplication workflow recommended. May affect coverage rate by 0.3%.'
    },
    {
        'id': 4,
        'type': 'Warning',
        'category': 'Dose Interval Too Short',
        'count': 11,
        'description': 'Second dose given earlier than recommended',
        'impact': 'Medium - Clinical protocol deviation',
        'ai_explanation': 'These patients received second doses 7-14 days early. All cases occurred at the same clinic during week of 12/15, suggesting systematic scheduling issue.',
        'recommendation': 'Notify clinic of protocol deviation. Clinical review to determine if revaccination needed.'
    },
    {
        'id': 5,
        'type': 'Warning',
        'category': 'Incomplete Data',
        'count': 21,
        'description': 'Missing batch numbers or lot IDs',
        'impact': 'Medium - Traceability concerns',
        'ai_explanation': 'Batch information missing from 21 recent entries. All from mobile vaccination unit operations. Prevents recall traceability.',
        'recommendation': 'Update mobile unit data entry protocol. Batch information must be mandatory field.'
    }
]

trend_data = pd.DataFrame([
    {'month': 'Aug', 'quality': 94.2, 'issues': 89},
    {'month': 'Sep', 'quality': 95.8, 'issues': 67},
    {'month': 'Oct', 'quality': 96.5, 'issues': 54},
    {'month': 'Nov', 'quality': 97.1, 'issues': 42},
    {'month': 'Dec', 'quality': 97.8, 'issues': 23}
])

# Header section
st.markdown("""
    <div style='background-color: white; padding: 24px; border-radius: 12px; 
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 24px;'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div>
                <h1 style='color: #1F2937; margin: 0; display: flex; align-items: center;'>
                    ⚡ Public Health Data Quality Guardian
                </h1>
                <p style='color: #6B7280; margin-top: 8px; margin-bottom: 0;'>
                    AI-powered vaccination data monitoring • Powered by Snowflake Intelligence
                </p>
            </div>
            <div style='text-align: right;'>
                <p style='color: #6B7280; font-size: 14px; margin: 0;'>Last Updated</p>
                <p style='color: #1F2937; font-size: 18px; font-weight: 600; margin: 0;'>2 minutes ago</p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Navigation tabs
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🔍 Anomaly Detection", "📄 AI Summary"])

# ==================== TAB 1: DASHBOARD ====================
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div style='background-color: white; padding: 24px; border-radius: 12px; 
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-left: 4px solid #10B981;'>
                <p style='color: #6B7280; font-size: 14px; font-weight: 500; margin: 0;'>Data Quality Score</p>
                <p style='color: #1F2937; font-size: 36px; font-weight: bold; margin: 8px 0;'>
                    {dashboard_stats['quality_score']}%
                </p>
                <p style='color: #10B981; font-size: 12px; margin: 0;'>↑ 0.7% from last month</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div style='background-color: white; padding: 24px; border-radius: 12px; 
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-left: 4px solid #3B82F6;'>
                <p style='color: #6B7280; font-size: 14px; font-weight: 500; margin: 0;'>Total Records</p>
                <p style='color: #1F2937; font-size: 36px; font-weight: bold; margin: 8px 0;'>
                    {dashboard_stats['total_records']:,}
                </p>
                <p style='color: #6B7280; font-size: 12px; margin: 0;'>Across all facilities</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div style='background-color: white; padding: 24px; border-radius: 12px; 
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-left: 4px solid #EF4444;'>
                <p style='color: #6B7280; font-size: 14px; font-weight: 500; margin: 0;'>Critical Issues</p>
                <p style='color: #1F2937; font-size: 36px; font-weight: bold; margin: 8px 0;'>
                    {dashboard_stats['critical_issues']}
                </p>
                <p style='color: #EF4444; font-size: 12px; margin: 0;'>Requires immediate action</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div style='background-color: white; padding: 24px; border-radius: 12px; 
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-left: 4px solid #F59E0B;'>
                <p style='color: #6B7280; font-size: 14px; font-weight: 500; margin: 0;'>Warnings</p>
                <p style='color: #1F2937; font-size: 36px; font-weight: bold; margin: 8px 0;'>
                    {dashboard_stats['warning_issues']}
                </p>
                <p style='color: #F59E0B; font-size: 12px; margin: 0;'>Review recommended</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Trend Chart
    st.markdown("""
        <div style='background-color: white; padding: 24px; border-radius: 12px; 
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
            <h3 style='color: #1F2937; margin-top: 0;'>Quality Trend (5 Months)</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Plotly chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=trend_data['month'],
        y=trend_data['quality'],
        name='Quality Score (%)',
        marker_color='rgb(16, 185, 129)',
        yaxis='y'
    ))
    
    fig.add_trace(go.Scatter(
        x=trend_data['month'],
        y=trend_data['issues'],
        name='Issues',
        mode='lines+markers',
        line=dict(color='rgb(239, 68, 68)', width=3),
        marker=dict(size=8),
        yaxis='y2'
    ))
    
    fig.update_layout(
        yaxis=dict(title='Quality Score (%)', side='left', range=[90, 100]),
        yaxis2=dict(title='Number of Issues', overlaying='y', side='right', range=[0, 100]),
        hovermode='x unified',
        height=400,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Monthly Progress Bars
    st.markdown("<br>", unsafe_allow_html=True)
    for _, row in trend_data.iterrows():
        col1, col2 = st.columns([1, 5])
        with col1:
            st.markdown(f"**{row['month']} 2024**")
        with col2:
            st.progress(row['quality'] / 100)
            st.caption(f"Quality: {row['quality']}% • Issues: {row['issues']}")

# ==================== TAB 2: ANOMALY DETECTION ====================
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    
    for anomaly in anomalies:
        emoji = '🔴' if anomaly['type'] == 'Critical' else '🟡'
        
        with st.expander(
            f"{emoji} **{anomaly['category']}** - {anomaly['description']}",
            expanded=False
        ):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown("#### Patient ID Information")
                st.code(f"Affected Records: {anomaly['count']}")
                
                st.markdown("#### 🤖 AI Analysis")
                st.info(anomaly['ai_explanation'])
                
                st.markdown("#### ✅ Recommended Action")
                st.success(anomaly['recommendation'])
            
            with col2:
                st.metric("Severity", anomaly['type'])
                st.metric("Impact", anomaly['impact'].split(' - ')[0])
                st.metric("Count", f"{anomaly['count']} records")
                
                if st.button(f"Mark Resolved", key=f"resolve_{anomaly['id']}"):
                    st.success("✓ Issue marked as resolved!")
                    st.balloons()

# ==================== TAB 3: AI SUMMARY ====================
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Executive Summary
    st.markdown("""
        <div style='background-color: #EFF6FF; border-left: 4px solid #2563EB; 
                    padding: 24px; border-radius: 8px; margin: 24px 0;'>
            <h3 style='color: #1E3A8A; margin-top: 0;'>Executive Summary</h3>
            <p style='color: #1E40AF; margin-bottom: 0; line-height: 1.6;'>
                Overall data quality continues to improve, reaching 97.8% this week. However, 23 critical 
                issues require immediate attention, primarily related to follow-up scheduling and data entry 
                accuracy. Two systematic issues were identified that affect multiple records.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Key Findings")
    
    # Priority 1
    st.markdown("""
        <div style='background-color: #FEE2E2; padding: 20px; border-radius: 8px; margin: 16px 0;'>
            <h4 style='color: #7F1D1D; margin-top: 0;'>Priority 1: Missing Second Doses</h4>
            <p style='color: #991B1B; margin-bottom: 0; line-height: 1.6;'>
                12 patients are significantly overdue for their second vaccination dose. AI analysis reveals 
                this is primarily due to follow-up system failures rather than patient non-compliance. 
                Automated contact lists have been generated for immediate outreach.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Priority 2
    st.markdown("""
        <div style='background-color: #FEF3C7; padding: 20px; border-radius: 8px; margin: 16px 0;'>
            <h4 style='color: #78350F; margin-top: 0;'>Priority 2: Systematic Scheduling Error</h4>
            <p style='color: #92400E; margin-bottom: 0; line-height: 1.6;'>
                A pattern of early second-dose administration was detected at one clinic location during 
                a specific week. This represents a systematic protocol deviation requiring clinical review 
                and staff retraining.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Positive Trend
    st.markdown("""
        <div style='background-color: #D1FAE5; padding: 20px; border-radius: 8px; margin: 16px 0;'>
            <h4 style='color: #064E3B; margin-top: 0;'>Positive Trend: Mobile Unit Improvement</h4>
            <p style='color: #065F46; margin-bottom: 0; line-height: 1.6;'>
                Data quality from mobile vaccination units has improved by 15% over the past month following 
                the implementation of mandatory field validation. Continue this approach.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Recommended Actions")
    
    actions = [
        "Immediately contact 12 patients overdue for second doses using generated priority list",
        "Conduct clinical review of 11 early second-dose cases for efficacy assessment",
        "Implement mandatory batch number fields for all vaccination entries",
        "Review and update patient matching algorithm to reduce duplicate entries",
        "Schedule training session for clinic staff on proper scheduling protocols"
    ]
    
    for i, action in enumerate(actions, 1):
        st.markdown(f"{i}. {action}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Report metadata
    st.markdown("""
        <div style='background-color: #F3F4F6; padding: 20px; border-radius: 8px;'>
            <p style='color: #4B5563; font-size: 14px; margin: 0;'>
                <strong>Report generated by:</strong> Snowflake Cortex AI | 
                <strong>Data as of:</strong> January 4, 2026 | 
                <strong>Next automated analysis:</strong> January 11, 2026
            </p>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.divider()
st.caption("Public Health Data Quality Guardian v1.0 | Powered by Snowflake & Streamlit")