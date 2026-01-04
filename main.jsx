import React, { useState } from 'react';
import { AlertTriangle, CheckCircle, TrendingUp, Users, Calendar, Activity, Search, FileText, BarChart3 } from 'lucide-react';

export default function HealthDataGuardian() {
  const [selectedView, setSelectedView] = useState('dashboard');
  const [selectedAnomaly, setSelectedAnomaly] = useState(null);

  // Simulated data from Snowflake queries
  const dashboardStats = {
    totalRecords: 45821,
    criticalIssues: 23,
    warningIssues: 47,
    cleanRecords: 45751,
    qualityScore: 97.8
  };

  const anomalies = [
    {
      id: 1,
      type: 'Critical',
      category: 'Missing Second Dose',
      count: 12,
      description: 'Patients overdue for second dose by >30 days',
      impact: 'High - Incomplete vaccination coverage',
      aiExplanation: 'These 12 patients received their first dose but are significantly overdue for the second dose. Analysis shows 8 were due to follow-up failures, 3 to address changes, and 1 to data entry error.',
      recommendation: 'Immediate outreach required. Priority contact list generated.'
    },
    {
      id: 2,
      type: 'Critical',
      category: 'Age Mismatch',
      count: 8,
      description: 'Vaccination age conflicts with birth records',
      impact: 'High - Data integrity issue',
      aiExplanation: 'Detected inconsistencies between vaccination dates and ages. 5 cases show impossible timelines (vaccination before birth), 3 cases have data entry errors in birth year.',
      recommendation: 'Manual review required. Likely data entry errors in patient ID or DOB fields.'
    },
    {
      id: 3,
      type: 'Warning',
      category: 'Duplicate Records',
      count: 15,
      description: 'Potential duplicate patient entries',
      impact: 'Medium - Inflated coverage statistics',
      aiExplanation: 'Found 15 patient records with matching names and similar DOBs across different IDs. Pattern suggests potential duplicate registrations during high-volume vaccination events.',
      recommendation: 'De-duplication workflow recommended. May affect coverage rate by 0.3%.'
    },
    {
      id: 4,
      type: 'Warning',
      category: 'Dose Interval Too Short',
      count: 11,
      description: 'Second dose given earlier than recommended',
      impact: 'Medium - Clinical protocol deviation',
      aiExplanation: 'These patients received second doses 7-14 days early. All cases occurred at the same clinic during week of 12/15, suggesting systematic scheduling issue.',
      recommendation: 'Notify clinic of protocol deviation. Clinical review to determine if revaccination needed.'
    },
    {
      id: 5,
      type: 'Warning',
      category: 'Incomplete Data',
      count: 21,
      description: 'Missing batch numbers or lot IDs',
      impact: 'Medium - Traceability concerns',
      aiExplanation: 'Batch information missing from 21 recent entries. All from mobile vaccination unit operations. Prevents recall traceability.',
      recommendation: 'Update mobile unit data entry protocol. Batch information must be mandatory field.'
    }
  ];

  const trendData = [
    { month: 'Aug', quality: 94.2, issues: 89 },
    { month: 'Sep', quality: 95.8, issues: 67 },
    { month: 'Oct', quality: 96.5, issues: 54 },
    { month: 'Nov', quality: 97.1, issues: 42 },
    { month: 'Dec', quality: 97.8, issues: 23 }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-800 flex items-center gap-3">
                <Activity className="text-blue-600" size={36} />
                Public Health Data Quality Guardian
              </h1>
              <p className="text-gray-600 mt-2">
                AI-powered vaccination data monitoring • Powered by Snowflake Intelligence
              </p>
            </div>
            <div className="text-right">
              <div className="text-sm text-gray-500">Last Updated</div>
              <div className="text-lg font-semibold text-gray-800">2 minutes ago</div>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <div className="flex gap-3 mb-6">
          <button
            onClick={() => setSelectedView('dashboard')}
            className={`px-6 py-3 rounded-lg font-semibold transition-all ${
              selectedView === 'dashboard'
                ? 'bg-blue-600 text-white shadow-lg'
                : 'bg-white text-gray-700 hover:bg-gray-50'
            }`}
          >
            <BarChart3 className="inline mr-2" size={20} />
            Dashboard
          </button>
          <button
            onClick={() => setSelectedView('anomalies')}
            className={`px-6 py-3 rounded-lg font-semibold transition-all ${
              selectedView === 'anomalies'
                ? 'bg-blue-600 text-white shadow-lg'
                : 'bg-white text-gray-700 hover:bg-gray-50'
            }`}
          >
            <Search className="inline mr-2" size={20} />
            Anomaly Detection
          </button>
          <button
            onClick={() => setSelectedView('report')}
            className={`px-6 py-3 rounded-lg font-semibold transition-all ${
              selectedView === 'report'
                ? 'bg-blue-600 text-white shadow-lg'
                : 'bg-white text-gray-700 hover:bg-gray-50'
            }`}
          >
            <FileText className="inline mr-2" size={20} />
            AI Summary
          </button>
        </div>

        {/* Dashboard View */}
        {selectedView === 'dashboard' && (
          <div className="space-y-6">
            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="bg-white rounded-xl p-6 shadow-lg border-l-4 border-green-500">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-500 font-medium">Data Quality Score</p>
                    <p className="text-3xl font-bold text-gray-800 mt-1">
                      {dashboardStats.qualityScore}%
                    </p>
                  </div>
                  <CheckCircle className="text-green-500" size={40} />
                </div>
                <p className="text-xs text-green-600 mt-2">↑ 0.7% from last month</p>
              </div>

              <div className="bg-white rounded-xl p-6 shadow-lg border-l-4 border-blue-500">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-500 font-medium">Total Records</p>
                    <p className="text-3xl font-bold text-gray-800 mt-1">
                      {dashboardStats.totalRecords.toLocaleString()}
                    </p>
                  </div>
                  <Users className="text-blue-500" size={40} />
                </div>
                <p className="text-xs text-gray-500 mt-2">Across all facilities</p>
              </div>

              <div className="bg-white rounded-xl p-6 shadow-lg border-l-4 border-red-500">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-500 font-medium">Critical Issues</p>
                    <p className="text-3xl font-bold text-gray-800 mt-1">
                      {dashboardStats.criticalIssues}
                    </p>
                  </div>
                  <AlertTriangle className="text-red-500" size={40} />
                </div>
                <p className="text-xs text-red-600 mt-2">Requires immediate action</p>
              </div>

              <div className="bg-white rounded-xl p-6 shadow-lg border-l-4 border-yellow-500">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-500 font-medium">Warnings</p>
                    <p className="text-3xl font-bold text-gray-800 mt-1">
                      {dashboardStats.warningIssues}
                    </p>
                  </div>
                  <TrendingUp className="text-yellow-500" size={40} />
                </div>
                <p className="text-xs text-yellow-600 mt-2">Review recommended</p>
              </div>
            </div>

            {/* Trend Chart */}
            <div className="bg-white rounded-xl p-6 shadow-lg">
              <h3 className="text-xl font-bold text-gray-800 mb-4">Quality Trend (5 Months)</h3>
              <div className="space-y-4">
                {trendData.map((data, idx) => (
                  <div key={idx}>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium text-gray-700">{data.month} 2024</span>
                      <div className="flex gap-4">
                        <span className="text-sm text-green-600 font-semibold">{data.quality}%</span>
                        <span className="text-sm text-gray-500">{data.issues} issues</span>
                      </div>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-3">
                      <div
                        className="bg-gradient-to-r from-green-500 to-green-600 h-3 rounded-full transition-all"
                        style={{ width: `${data.quality}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Anomalies View */}
        {selectedView === 'anomalies' && (
          <div className="space-y-4">
            {anomalies.map((anomaly) => (
              <div
                key={anomaly.id}
                className="bg-white rounded-xl p-6 shadow-lg cursor-pointer hover:shadow-xl transition-shadow"
                onClick={() => setSelectedAnomaly(selectedAnomaly?.id === anomaly.id ? null : anomaly)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <span
                        className={`px-3 py-1 rounded-full text-xs font-bold ${
                          anomaly.type === 'Critical'
                            ? 'bg-red-100 text-red-700'
                            : 'bg-yellow-100 text-yellow-700'
                        }`}
                      >
                        {anomaly.type}
                      </span>
                      <h3 className="text-lg font-bold text-gray-800">{anomaly.category}</h3>
                    </div>
                    <p className="text-gray-600 mb-2">{anomaly.description}</p>
                    <div className="flex items-center gap-4 text-sm">
                      <span className="text-gray-500">
                        <strong>Affected Records:</strong> {anomaly.count}
                      </span>
                      <span className="text-gray-500">
                        <strong>Impact:</strong> {anomaly.impact}
                      </span>
                    </div>
                  </div>
                  <AlertTriangle
                    className={anomaly.type === 'Critical' ? 'text-red-500' : 'text-yellow-500'}
                    size={32}
                  />
                </div>

                {selectedAnomaly?.id === anomaly.id && (
                  <div className="mt-6 pt-6 border-t border-gray-200">
                    <div className="bg-blue-50 rounded-lg p-4 mb-4">
                      <h4 className="font-bold text-blue-900 mb-2 flex items-center gap-2">
                        <Activity size={18} />
                        AI Analysis
                      </h4>
                      <p className="text-blue-800 text-sm leading-relaxed">
                        {anomaly.aiExplanation}
                      </p>
                    </div>
                    <div className="bg-green-50 rounded-lg p-4">
                      <h4 className="font-bold text-green-900 mb-2 flex items-center gap-2">
                        <CheckCircle size={18} />
                        Recommended Action
                      </h4>
                      <p className="text-green-800 text-sm leading-relaxed">
                        {anomaly.recommendation}
                      </p>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        {/* AI Summary View */}
        {selectedView === 'report' && (
          <div className="bg-white rounded-xl p-8 shadow-lg">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">
              Weekly AI-Generated Summary Report
            </h2>
            
            <div className="prose prose-blue max-w-none">
              <div className="bg-blue-50 border-l-4 border-blue-600 p-6 mb-6">
                <h3 className="text-xl font-bold text-blue-900 mt-0">Executive Summary</h3>
                <p className="text-blue-800 mb-0">
                  Overall data quality continues to improve, reaching 97.8% this week. However, 23 critical 
                  issues require immediate attention, primarily related to follow-up scheduling and data entry 
                  accuracy. Two systematic issues were identified that affect multiple records.
                </p>
              </div>

              <h3 className="text-lg font-bold text-gray-800">Key Findings</h3>
              
              <div className="bg-red-50 rounded-lg p-4 mb-4">
                <h4 className="text-red-900 font-bold">Priority 1: Missing Second Doses</h4>
                <p className="text-red-800">
                  12 patients are significantly overdue for their second vaccination dose. AI analysis reveals 
                  this is primarily due to follow-up system failures rather than patient non-compliance. 
                  Automated contact lists have been generated for immediate outreach.
                </p>
              </div>

              <div className="bg-yellow-50 rounded-lg p-4 mb-4">
                <h4 className="text-yellow-900 font-bold">Priority 2: Systematic Scheduling Error</h4>
                <p className="text-yellow-800">
                  A pattern of early second-dose administration was detected at one clinic location during 
                  a specific week. This represents a systematic protocol deviation requiring clinical review 
                  and staff retraining.
                </p>
              </div>

              <div className="bg-green-50 rounded-lg p-4 mb-4">
                <h4 className="text-green-900 font-bold">Positive Trend: Mobile Unit Improvement</h4>
                <p className="text-green-800">
                  Data quality from mobile vaccination units has improved by 15% over the past month following 
                  the implementation of mandatory field validation. Continue this approach.
                </p>
              </div>

              <h3 className="text-lg font-bold text-gray-800 mt-6">Recommended Actions</h3>
              <ol className="text-gray-700 space-y-2">
                <li>Immediately contact 12 patients overdue for second doses using generated priority list</li>
                <li>Conduct clinical review of 11 early second-dose cases for efficacy assessment</li>
                <li>Implement mandatory batch number fields for all vaccination entries</li>
                <li>Review and update patient matching algorithm to reduce duplicate entries</li>
                <li>Schedule training session for clinic staff on proper scheduling protocols</li>
              </ol>

              <div className="bg-gray-100 rounded-lg p-4 mt-6">
                <p className="text-sm text-gray-600 mb-0">
                  <strong>Report generated by:</strong> Snowflake Cortex AI | <strong>Data as of:</strong> January 4, 2026 
                  | <strong>Next automated analysis:</strong> January 11, 2026
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}