"""CSS styles for the application"""
def get_css() -> str:
    """Get CSS styles (simplified, no dark mode)"""
    return """
    <style>
    /* General */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Header */
    .hero {
        padding: 2rem 2.5rem;
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.5);
        margin-bottom: 2rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    .hero h1 {
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
    }
    .hero p {
        margin: 0.5rem 0 0;
        opacity: 0.8;
        font-size: 1.1rem;
    }
    
    /* Pills */
    .pill {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 999px;
        border: 1px solid rgba(0, 0, 0, 0.1);
        font-size: 0.9rem;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        transition: all 0.2s ease;
        background: rgba(255, 255, 255, 0.8);
    }
    .pill:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Career Path Cards */
    .career-card {
        border: 2px solid rgba(0, 0, 0, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        background: rgba(255, 255, 255, 0.8);
        margin: 0.5rem;
        transition: all 0.3s ease;
        cursor: pointer;
        min-width: 200px;
    }
    .career-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        border-color: #10B981;
    }
    .career-card.active {
        border-color: #10B981;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(16, 185, 129, 0.1) 100%);
    }
    .career-card h4 {
        margin: 0 0 0.5rem 0;
        font-size: 1.2rem;
    }
    .career-card .summary {
        opacity: 0.8;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Career Path with Connected Bullets */
    .career-path-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 2rem 0;
        position: relative;
    }
    
    .career-path-item {
        position: relative;
        width: 100%;
        max-width: 400px;
        margin: 0.5rem 0;
    }
    
    .career-path-card {
        border: 2px solid rgba(0, 0, 0, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        background: rgba(255, 255, 255, 0.9);
        transition: all 0.3s ease;
        cursor: pointer;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .career-path-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        border-color: #10B981;
    }
    
    .career-path-card.active {
        border-color: #10B981;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(16, 185, 129, 0.15) 100%);
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.2);
    }
    
    .career-path-card h4 {
        margin: 0 0 0.5rem 0;
        font-size: 1.3rem;
        color: #1E1E1E;
    }
    
    .career-path-card .summary {
        opacity: 0.8;
        font-size: 0.95rem;
        margin: 0.5rem 0;
        line-height: 1.5;
    }
    
    .career-path-card .stats {
        display: flex;
        gap: 1rem;
        margin-top: 0.75rem;
        font-size: 0.85rem;
        opacity: 0.7;
    }
    
    .career-path-bullet {
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
        width: 16px;
        height: 16px;
        border-radius: 50%;
        background: #10B981;
        border: 3px solid white;
        z-index: 2;
        box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.3);
    }
    
    .career-path-bullet.top {
        top: -8px;
    }
    
    .career-path-bullet.bottom {
        bottom: -8px;
    }
    
    .career-path-line {
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
        width: 3px;
        height: 30px;
        background: linear-gradient(to bottom, #10B981, rgba(16, 185, 129, 0.3));
        z-index: 1;
    }
    
    .career-path-line.top {
        top: -30px;
    }
    
    .career-path-line.bottom {
        bottom: -30px;
    }
    
    /* Horizontal layout for many levels */
    .career-path-horizontal {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        flex-wrap: wrap;
        gap: 1rem;
        padding: 2rem 0;
        position: relative;
    }
    
    .career-path-horizontal .career-path-item {
        max-width: 220px;
        min-width: 200px;
    }
    
    .career-path-horizontal .career-path-line {
        width: 40px;
        height: 3px;
        top: 50%;
        transform: translateY(-50%);
        left: auto;
        right: -20px;
    }
    
    .career-path-horizontal .career-path-bullet {
        top: 50%;
        transform: translateY(-50%);
        left: auto;
        right: -8px;
    }
    
    /* Career Path Grid */
    .career-path-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        padding: 1rem 0;
    }
    
    /* Skill item */
    .skill {
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        background: rgba(255, 255, 255, 0.6);
        margin-bottom: 1rem;
        transition: all 0.2s ease;
    }
    .skill:hover {
        border-color: #10B981;
        transform: translateX(4px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    .skill-title {
        font-weight: 700;
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
    }
    .muted {
        opacity: 0.8;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Chips */
    .chip {
        display: inline-block;
        padding: 0.25rem 0.7rem;
        border-radius: 999px;
        font-size: 0.8rem;
        border: 1px solid rgba(0, 0, 0, 0.1);
        margin-right: 0.5rem;
        margin-top: 0.3rem;
        background: rgba(255, 255, 255, 0.8);
    }
    
    /* Comparison tags */
    .tag-new {
        border-color: #10B981;
        background: rgba(16, 185, 129, 0.1);
        color: #10B981;
    }
    .tag-deepen {
        border-color: #F59E0B;
        background: rgba(245, 158, 11, 0.1);
        color: #F59E0B;
    }
    .tag-common {
        border-color: rgba(148, 163, 184, 0.6);
        background: rgba(148, 163, 184, 0.1);
        color: rgba(148, 163, 184, 0.8);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    .fade-in {
        animation: fadeIn 0.4s ease-out;
    }
    
    /* Section spacing */
    .section-spacing {
        margin: 2rem 0;
    }
    
    /* Career path cards */
    .stContainer {
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-radius: 12px;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.5);
        margin-bottom: 1rem;
        transition: all 0.2s ease;
    }
    
    .stContainer:hover {
        border-color: #10B981;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* Comparison section cards */
    .comparison-section {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border: 2px solid rgba(0, 0, 0, 0.1);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .comparison-section.new {
        border-color: #10B981;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(16, 185, 129, 0.05) 100%);
    }
    
    .comparison-section.deepen {
        border-color: #F59E0B;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(245, 158, 11, 0.05) 100%);
    }
    
    .comparison-section.common {
        border-color: rgba(148, 163, 184, 0.6);
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(148, 163, 184, 0.05) 100%);
    }
    
    .comparison-section h4 {
        margin: 0 0 1rem 0;
        font-size: 1.3rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .comparison-section .icon {
        font-size: 1.5rem;
    }
    </style>
    """
