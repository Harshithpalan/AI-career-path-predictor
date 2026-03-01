import requests
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import numpy as np
from collections import Counter
import os
from dotenv import load_dotenv

load_dotenv()

class GitHubAnalyzer:
    def __init__(self):
        self.api_token = os.getenv("GITHUB_TOKEN")
        self.headers = {
            "Authorization": f"token {self.api_token}",
            "Accept": "application/vnd.github.v3+json"
        } if self.api_token else {}
        self.base_url = "https://api.github.com"
        
        # Language categories for orientation scoring
        self.ml_languages = {'python', 'r', 'jupyter-notebook', 'tensorflow', 'pytorch'}
        self.web_languages = {'javascript', 'typescript', 'html', 'css', 'react', 'vue', 'angular'}
        self.systems_languages = {'c', 'c++', 'rust', 'go', 'assembly', 'shell'}
        
    def get_user_profile(self, username: str) -> Dict[str, Any]:
        """Get basic GitHub user profile"""
        url = f"{self.base_url}/users/{username}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 404:
            raise ValueError(f"GitHub user '{username}' not found")
        elif response.status_code != 200:
            raise Exception(f"GitHub API error: {response.status_code}")
        
        return response.json()
    
    def get_user_repos(self, username: str, repo_type: str = "all") -> List[Dict[str, Any]]:
        """Get user repositories"""
        url = f"{self.base_url}/users/{username}/repos"
        params = {
            "type": repo_type,
            "sort": "updated",
            "per_page": 100
        }
        
        repos = []
        page = 1
        
        while True:
            params["page"] = page
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code != 200:
                break
            
            page_repos = response.json()
            if not page_repos:
                break
            
            repos.extend(page_repos)
            page += 1
            
            if len(repos) >= 500:  # GitHub limit
                break
        
        return repos
    
    def get_repo_languages(self, username: str, repo_name: str) -> Dict[str, int]:
        """Get language statistics for a repository"""
        url = f"{self.base_url}/repos/{username}/{repo_name}/languages"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code != 200:
            return {}
        
        return response.json()
    
    def get_commit_activity(self, username: str, repo_name: str) -> List[Dict[str, Any]]:
        """Get commit activity for a repository"""
        url = f"{self.base_url}/repos/{username}/{repo_name}/stats/commit_activity"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code != 200:
            return []
        
        return response.json()
    
    def analyze_languages(self, repos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze programming languages across repositories"""
        language_stats = Counter()
        language_bytes = {}
        
        for repo in repos:
            if not repo.get("language"):
                continue
            
            # Simple language counting
            lang = repo["language"]
            language_stats[lang] += 1
            
            # Get detailed language stats if possible
            try:
                repo_languages = self.get_repo_languages(repo["owner"]["login"], repo["name"])
                for lang, bytes_count in repo_languages.items():
                    if lang not in language_bytes:
                        language_bytes[lang] = 0
                    language_bytes[lang] += bytes_count
            except:
                continue
        
        # Calculate percentages
        total_bytes = sum(language_bytes.values()) if language_bytes else 1
        language_percentages = {
            lang: (bytes_count / total_bytes) * 100 
            for lang, bytes_count in language_bytes.items()
        }
        
        # Sort by percentage
        sorted_languages = sorted(
            language_percentages.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        return {
            "primary_languages": [lang for lang, _ in sorted_languages[:5]],
            "language_percentages": dict(sorted_languages),
            "language_diversity": len(language_stats),
            "total_bytes": total_bytes
        }
    
    def calculate_orientation_scores(self, language_percentages: Dict[str, float]) -> Dict[str, float]:
        """Calculate orientation scores based on language usage"""
        ml_score = 0.0
        web_score = 0.0
        systems_score = 0.0
        
        for lang, percentage in language_percentages.items():
            lang_lower = lang.lower()
            
            if lang_lower in self.ml_languages:
                ml_score += percentage
            elif lang_lower in self.web_languages:
                web_score += percentage
            elif lang_lower in self.systems_languages:
                systems_score += percentage
        
        # Normalize to 0-1 scale
        max_score = max(ml_score, web_score, systems_score, 1.0)
        
        return {
            "ml_orientation": ml_score / max_score,
            "web_orientation": web_score / max_score,
            "systems_orientation": systems_score / max_score
        }
    
    def analyze_commit_patterns(self, username: str, repos: List[Dict[str, Any]]) -> Dict[str, float]:
        """Analyze commit patterns and consistency"""
        if not repos:
            return {"commit_frequency": 0.5, "contribution_consistency": 0.5}
        
        total_commits = 0
        active_weeks = set()
        weekly_contributions = []
        
        # Analyze up to 10 most recent repos
        for repo in repos[:10]:
            try:
                commit_activity = self.get_commit_activity(username, repo["name"])
                
                for week_data in commit_activity:
                    week_commits = sum(week_data.get("days", []))
                    if week_commits > 0:
                        total_commits += week_commits
                        active_weeks.add(week_data.get("week", 0))
                        weekly_contributions.append(week_commits)
                        
            except:
                continue
        
        # Calculate metrics
        commit_frequency = min(1.0, total_commits / (len(repos) * 100))  # Normalize
        
        if weekly_contributions:
            avg_weekly = np.mean(weekly_contributions)
            std_weekly = np.std(weekly_contributions)
            consistency = 1.0 - (std_weekly / (avg_weekly + 1))  # Lower std = higher consistency
            contribution_consistency = max(0.0, min(1.0, consistency))
        else:
            contribution_consistency = 0.5
        
        return {
            "commit_frequency": commit_frequency,
            "contribution_consistency": contribution_consistency,
            "total_commits": total_commits,
            "active_weeks": len(active_weeks)
        }
    
    def calculate_project_complexity(self, repos: List[Dict[str, Any]]) -> float:
        """Calculate project complexity score based on repository characteristics"""
        if not repos:
            return 0.5
        
        complexity_scores = []
        
        for repo in repos:
            score = 0.0
            
            # Fork vs original (original gets higher score)
            if not repo.get("fork", True):
                score += 0.3
            
            # Repository size (approximate by stars and forks)
            stars = repo.get("stargazers_count", 0)
            forks = repo.get("forks_count", 0)
            watchers = repo.get("watchers_count", 0)
            
            # Normalize and weight
            star_score = min(1.0, stars / 100) * 0.2
            fork_score = min(1.0, forks / 20) * 0.1
            watcher_score = min(1.0, watchers / 10) * 0.1
            
            score += star_score + fork_score + watcher_score
            
            # Has issues (indicates active project)
            if repo.get("open_issues_count", 0) > 0:
                score += 0.1
            
            # Has README (indicates well-documented)
            if repo.get("has_readme", False):
                score += 0.1
            
            # Has wiki or pages
            if repo.get("has_wiki", False) or repo.get("has_pages", False):
                score += 0.1
            
            complexity_scores.append(min(1.0, score))
        
        return np.mean(complexity_scores) if complexity_scores else 0.5
    
    def calculate_innovation_score(self, repos: List[Dict[str, Any]], language_analysis: Dict[str, Any]) -> float:
        """Calculate innovation score based on technology diversity and project uniqueness"""
        if not repos:
            return 0.5
        
        innovation_score = 0.0
        
        # Language diversity (more diverse = more innovative)
        language_diversity = language_analysis.get("language_diversity", 1)
        diversity_score = min(1.0, language_diversity / 5) * 0.3
        innovation_score += diversity_score
        
        # Original projects (not forks)
        original_projects = sum(1 for repo in repos if not repo.get("fork", True))
        originality_score = min(1.0, original_projects / len(repos)) * 0.4
        innovation_score += originality_score
        
        # Project topics/keywords (indicates modern tech)
        total_topics = 0
        modern_tech_keywords = ['ai', 'ml', 'blockchain', 'cloud', 'kubernetes', 'docker', 'microservices']
        
        for repo in repos:
            topics = repo.get("topics", [])
            total_topics += len(topics)
            
            # Check for modern tech keywords in topics or description
            repo_text = f" {repo.get('description', '')} {' '.join(topics)} ".lower()
            for keyword in modern_tech_keywords:
                if keyword in repo_text:
                    innovation_score += 0.05
        
        # Cap the score
        return min(1.0, innovation_score)
    
    def analyze_github_profile(self, username: str) -> Dict[str, Any]:
        """Complete GitHub profile analysis"""
        try:
            # Get user profile
            user_profile = self.get_user_profile(username)
            
            # Get repositories
            repos = self.get_user_repos(username)
            
            # Analyze languages
            language_analysis = self.analyze_languages(repos)
            
            # Calculate orientation scores
            orientation_scores = self.calculate_orientation_scores(
                language_analysis.get("language_percentages", {})
            )
            
            # Analyze commit patterns
            commit_analysis = self.analyze_commit_patterns(username, repos)
            
            # Calculate project complexity
            complexity_score = self.calculate_project_complexity(repos)
            
            # Calculate innovation score
            innovation_score = self.calculate_innovation_score(repos, language_analysis)
            
            # Calculate overall scores
            consistency_score = commit_analysis.get("contribution_consistency", 0.5)
            depth_score = complexity_score
            
            # Overall GitHub score (weighted combination)
            overall_score = (
                consistency_score * 0.3 +
                depth_score * 0.3 +
                innovation_score * 0.2 +
                commit_analysis.get("commit_frequency", 0.5) * 0.2
            )
            
            return {
                "github_username": username,
                "total_repos": user_profile.get("total_private_repos", 0) + len(repos),
                "public_repos": len(repos),
                "followers": user_profile.get("followers", 0),
                "following": user_profile.get("following", 0),
                "total_commits": commit_analysis.get("total_commits", 0),
                "primary_languages": language_analysis.get("primary_languages", []),
                "language_percentages": language_analysis.get("language_percentages", {}),
                "commit_frequency": commit_analysis.get("commit_frequency", 0.5),
                "contribution_consistency": commit_analysis.get("contribution_consistency", 0.5),
                "project_complexity_score": complexity_score,
                "ml_orientation": orientation_scores.get("ml_orientation", 0.5),
                "web_orientation": orientation_scores.get("web_orientation", 0.5),
                "systems_orientation": orientation_scores.get("systems_orientation", 0.5),
                "innovation_score": innovation_score,
                "consistency_score": consistency_score,
                "depth_score": depth_score,
                "overall_github_score": round(overall_score, 3),
                "raw_profile": user_profile,
                "analysis_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            raise Exception(f"GitHub analysis failed: {str(e)}")
