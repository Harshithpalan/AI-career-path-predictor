from fastapi import APIRouter, HTTPException
from schemas.prediction import GitHubAnalysisInput, GitHubProfileResponse
from services.github_service import GitHubAnalyzer

router = APIRouter()
github_analyzer = GitHubAnalyzer()

@router.post("/analyze-github", response_model=GitHubProfileResponse)
async def analyze_github_profile(request: GitHubAnalysisInput):
    """Analyze GitHub profile and return comprehensive insights"""
    
    try:
        analysis_result = github_analyzer.analyze_github_profile(request.github_username)
        
        return GitHubProfileResponse(
            github_username=analysis_result['github_username'],
            total_repos=analysis_result['total_repos'],
            public_repos=analysis_result['public_repos'],
            followers=analysis_result['followers'],
            following=analysis_result['following'],
            total_commits=analysis_result['total_commits'],
            primary_languages=analysis_result['primary_languages'],
            language_percentages=analysis_result['language_percentages'],
            commit_frequency=analysis_result['commit_frequency'],
            contribution_consistency=analysis_result['contribution_consistency'],
            project_complexity_score=analysis_result['project_complexity_score'],
            ml_orientation=analysis_result['ml_orientation'],
            web_orientation=analysis_result['web_orientation'],
            systems_orientation=analysis_result['systems_orientation'],
            innovation_score=analysis_result['innovation_score'],
            consistency_score=analysis_result['consistency_score'],
            depth_score=analysis_result['depth_score'],
            overall_github_score=analysis_result['overall_github_score']
        )
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GitHub analysis failed: {str(e)}")

@router.get("/github/{username}")
async def get_github_summary(username: str):
    """Get basic GitHub profile summary"""
    
    try:
        profile = github_analyzer.get_user_profile(username)
        
        return {
            "username": profile.get('login'),
            "name": profile.get('name'),
            "bio": profile.get('bio'),
            "location": profile.get('location'),
            "public_repos": profile.get('public_repos', 0),
            "followers": profile.get('followers', 0),
            "following": profile.get('following', 0),
            "created_at": profile.get('created_at'),
            "updated_at": profile.get('updated_at')
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch GitHub profile: {str(e)}")

@router.get("/github/{username}/repos")
async def get_user_repositories(username: str, limit: int = 10):
    """Get user's repositories summary"""
    
    try:
        repos = github_analyzer.get_user_repos(username)
        
        repo_summaries = []
        for repo in repos[:limit]:
            repo_summaries.append({
                "name": repo.get('name'),
                "description": repo.get('description'),
                "language": repo.get('language'),
                "stars": repo.get('stargazers_count', 0),
                "forks": repo.get('forks_count', 0),
                "created_at": repo.get('created_at'),
                "updated_at": repo.get('updated_at'),
                "is_fork": repo.get('fork', False),
                "topics": repo.get('topics', [])
            })
        
        return {
            "username": username,
            "total_repos": len(repos),
            "repositories": repo_summaries
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch repositories: {str(e)}")
