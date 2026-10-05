"""
visualization.py
Helper functions for creating charts used in the Streamlit application.
Uses Plotly for interactive charts and Matplotlib/Seaborn for static plots.
"""

import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


# ── Plotly charts ──────────────────────────────────────────────────────

def plot_score_distribution(df):
    """Histogram of final exam scores coloured by performance category."""
    order = ["Excellent", "Good", "Average", "Needs Improvement"]
    fig = px.histogram(
        df, x="final_exam_score",
        color="performance_category",
        category_orders={"performance_category": order},
        nbins=30,
        title="Distribution of Final Exam Scores",
        labels={"final_exam_score": "Final Exam Score",
                "performance_category": "Category"},
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.update_layout(bargap=0.05)
    return fig


def plot_performance_pie(df):
    """Donut chart of performance category distribution."""
    counts = df["performance_category"].value_counts().reset_index()
    counts.columns = ["Category", "Count"]
    order = ["Excellent", "Good", "Average", "Needs Improvement"]
    counts["Category"] = pd.Categorical(counts["Category"],
                                         categories=order, ordered=True)
    counts = counts.sort_values("Category")
    fig = px.pie(
        counts, names="Category", values="Count",
        title="Performance Category Distribution",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    return fig


def plot_dept_avg_score(df):
    """Bar chart: average final exam score by department."""
    avg = df.groupby("department")["final_exam_score"].mean().reset_index()
    avg.columns = ["Department", "Avg Final Score"]
    avg = avg.sort_values("Avg Final Score", ascending=False)
    fig = px.bar(
        avg, x="Department", y="Avg Final Score",
        title="Average Final Exam Score by Department",
        color="Department",
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig.update_layout(showlegend=False)
    return fig


def plot_scatter(df, x_col, y_col, color_col="performance_category",
                 title=None):
    """Interactive scatter plot of two numerical columns."""
    if title is None:
        title = f"{x_col.replace('_', ' ').title()} vs {y_col.replace('_', ' ').title()}"
    fig = px.scatter(
        df, x=x_col, y=y_col, color=color_col,
        title=title,
        labels={x_col: x_col.replace("_", " ").title(),
                y_col: y_col.replace("_", " ").title()},
        opacity=0.6,
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    return fig


def plot_box_dept(df):
    """Box plot of final exam score by department."""
    fig = px.box(
        df, x="department", y="final_exam_score",
        color="department",
        title="Final Exam Score Distribution by Department",
        labels={"department": "Department",
                "final_exam_score": "Final Exam Score"},
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig.update_layout(showlegend=False)
    return fig


def plot_category_bar(df):
    """Bar chart of performance category counts."""
    order = ["Excellent", "Good", "Average", "Needs Improvement"]
    counts = df["performance_category"].value_counts().reindex(order).reset_index()
    counts.columns = ["Category", "Count"]
    fig = px.bar(
        counts, x="Category", y="Count",
        title="Number of Students per Performance Category",
        color="Category",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.update_layout(showlegend=False)
    return fig


def plot_avg_by_year(df):
    """Bar chart: average final exam score by year."""
    avg = df.groupby("year")["final_exam_score"].mean().reset_index()
    avg.columns = ["Year", "Avg Final Score"]
    avg["Year"] = avg["Year"].astype(str)
    fig = px.bar(
        avg, x="Year", y="Avg Final Score",
        title="Average Final Exam Score by Year",
        color="Year",
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig.update_layout(showlegend=False)
    return fig


def plot_attendance_by_dept(df):
    """Bar chart: average attendance by department."""
    avg = df.groupby("department")["attendance_percentage"].mean().reset_index()
    avg.columns = ["Department", "Avg Attendance (%)"]
    avg = avg.sort_values("Avg Attendance (%)", ascending=False)
    fig = px.bar(
        avg, x="Department", y="Avg Attendance (%)",
        title="Average Attendance by Department",
        color="Department",
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig.update_layout(showlegend=False)
    return fig


# ── Matplotlib / Seaborn charts ──────────────────────────────────────

def plot_correlation_heatmap(df):
    """Seaborn heatmap of numerical column correlations."""
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    corr = df[num_cols].corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm",
                linewidths=0.5, ax=ax)
    ax.set_title("Correlation Heatmap of Numerical Features", fontsize=14)
    plt.tight_layout()
    return fig


def plot_model_comparison(results_df):
    """Grouped bar chart comparing model metrics."""
    fig = go.Figure()
    metrics = ["MAE", "RMSE", "R²"]
    colors = ["#66c2a5", "#fc8d62", "#8da0cb"]
    for i, metric in enumerate(metrics):
        fig.add_trace(go.Bar(
            name=metric,
            x=results_df["Model"],
            y=results_df[metric],
            marker_color=colors[i],
        ))
    fig.update_layout(
        barmode="group",
        title="Model Performance Comparison",
        yaxis_title="Score",
        xaxis_title="Model",
    )
    return fig
