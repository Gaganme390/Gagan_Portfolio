/* =====================================================
   GITHUB.JS — GitHub API Integration
   ===================================================== */

class GitHubIntegration {
    constructor(username) {
        this.username = username;
        this.apiBase = 'https://api.github.com';
        this.container = document.getElementById('github-container');

        if (!this.container) return;

        if (!this.username) {
            this.showPlaceholder();
            return;
        }

        this.init();
    }

    async init() {
        try {
            const [profile, repos] = await Promise.all([
                this.fetchProfile(),
                this.fetchRepos(),
            ]);

            this.renderProfile(profile);
            this.renderStats(profile, repos);
            this.renderRepos(repos);
            this.renderLanguages(repos);
        } catch (error) {
            console.error('GitHub API error:', error);
            this.showPlaceholder();
        }
    }

    async fetchProfile() {
        const res = await fetch(`${this.apiBase}/users/${this.username}`);
        if (!res.ok) throw new Error('Failed to fetch profile');
        return res.json();
    }

    async fetchRepos() {
        const res = await fetch(
            `${this.apiBase}/users/${this.username}/repos?sort=updated&per_page=30`
        );
        if (!res.ok) throw new Error('Failed to fetch repos');
        return res.json();
    }

    renderProfile(profile) {
        const card = this.container.querySelector('.github-profile-card');
        if (!card) return;

        const avatar = card.querySelector('.github-avatar');
        if (profile.avatar_url) {
            avatar.innerHTML = `<img src="${profile.avatar_url}" alt="${profile.login}" style="width:100%;height:100%;border-radius:50%;object-fit:cover;">`;
        }

        const info = card.querySelector('.github-profile-info');
        if (info) {
            info.querySelector('h3').textContent = profile.name || profile.login;
            info.querySelector('p').textContent = profile.bio || 'Software Developer';
        }
    }

    renderStats(profile, repos) {
        const statsGrid = this.container.querySelector('.github-stats-grid');
        if (!statsGrid) return;

        const totalStars = repos.reduce((acc, repo) => acc + repo.stargazers_count, 0);
        const totalForks = repos.reduce((acc, repo) => acc + repo.forks_count, 0);

        const stats = [
            { value: profile.public_repos, label: 'Repositories' },
            { value: totalStars, label: 'Total Stars' },
            { value: totalForks, label: 'Total Forks' },
            { value: profile.followers, label: 'Followers' },
        ];

        statsGrid.innerHTML = stats.map(stat => `
            <div class="github-stat-card fade-in">
                <div class="github-stat-value" data-count="${stat.value}">0</div>
                <div class="github-stat-label">${stat.label}</div>
            </div>
        `).join('');

        // Animate counters
        setTimeout(() => {
            statsGrid.querySelectorAll('[data-count]').forEach(el => {
                const target = parseInt(el.dataset.count);
                animateValue(el, 0, target, 1500);
            });
        }, 300);
    }

    renderRepos(repos) {
        const reposContainer = this.container.querySelector('.github-repos');
        if (!reposContainer) return;

        const topRepos = repos
            .sort((a, b) => b.stargazers_count - a.stargazers_count)
            .slice(0, 6);

        reposContainer.innerHTML = topRepos.map(repo => `
            <a href="${repo.html_url}" target="_blank" rel="noopener" class="github-repo-card fade-in">
                <div class="github-repo-name">
                    📁 ${repo.name}
                </div>
                <p class="github-repo-desc">${repo.description || 'No description available'}</p>
                <div class="github-repo-meta">
                    ${repo.language ? `<span><span class="github-lang-dot" style="background:${this.getLanguageColor(repo.language)}"></span> ${repo.language}</span>` : ''}
                    <span>⭐ ${repo.stargazers_count}</span>
                    <span>🔀 ${repo.forks_count}</span>
                </div>
            </a>
        `).join('');
    }

    renderLanguages(repos) {
        const langContainer = this.container.querySelector('.github-languages');
        if (!langContainer) return;

        const langCount = {};
        repos.forEach(repo => {
            if (repo.language) {
                langCount[repo.language] = (langCount[repo.language] || 0) + 1;
            }
        });

        const total = Object.values(langCount).reduce((a, b) => a + b, 0);
        const sorted = Object.entries(langCount)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 8);

        langContainer.innerHTML = sorted.map(([lang, count]) => {
            const pct = Math.round((count / total) * 100);
            return `
                <div class="github-lang-item">
                    <span class="github-lang-dot" style="background:${this.getLanguageColor(lang)}"></span>
                    <span style="font-size:0.85rem;color:var(--text-secondary);min-width:80px">${lang}</span>
                    <div class="github-lang-bar">
                        <div class="github-lang-fill" style="width:${pct}%;background:${this.getLanguageColor(lang)}"></div>
                    </div>
                    <span style="font-size:0.8rem;color:var(--text-muted)">${pct}%</span>
                </div>
            `;
        }).join('');
    }

    getLanguageColor(lang) {
        const colors = {
            JavaScript: '#f1e05a',
            TypeScript: '#3178c6',
            Python: '#3572A5',
            HTML: '#e34c26',
            CSS: '#563d7c',
            Java: '#b07219',
            'C++': '#f34b7d',
            'C#': '#178600',
            PHP: '#4F5D95',
            Ruby: '#701516',
            Go: '#00ADD8',
            Rust: '#dea584',
            Shell: '#89e051',
            Dockerfile: '#384d54',
        };
        return colors[lang] || '#8b949e';
    }

    showPlaceholder() {
        const content = this.container.querySelector('.github-content');
        if (content) {
            content.innerHTML = `
                <div class="github-placeholder">
                    <p>🔗 GitHub integration will appear here once configured.</p>
                    <p style="font-size:0.85rem">Add your GitHub username in the Django Admin panel to enable this section.</p>
                </div>
            `;
        }
    }
}

function animateValue(el, start, end, duration) {
    const startTime = performance.now();
    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 4);
        el.textContent = Math.round(start + (end - start) * eased);
        if (progress < 1) requestAnimationFrame(update);
    }
    requestAnimationFrame(update);
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('github-container');
    if (container) {
        const username = container.dataset.username || '';
        new GitHubIntegration(username);
    }
});
