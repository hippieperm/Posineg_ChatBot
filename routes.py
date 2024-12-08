from flask import Blueprint, render_template
from flask_login import login_required, current_user
from stock_data import stock_data
from datetime import datetime

# Blueprint 설정
main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)

# 홈 페이지 라우트
@main.route('/')
def index():
    """홈페이지를 표시합니다."""
    try:
        # 기본 데이터 준비
        context = {
            'stocks': [],
            'portfolio': None
        }
        
        # 주식 데이터 가져오기 시도
        try:
            context['stocks'] = stock_data.get_all_stocks() if stock_data else []
        except Exception as stock_error:
            print(f"Error getting stock data: {str(stock_error)}")

        return render_template('home.html', **context)

    except Exception as e:
        print(f"Critical error in index route: {str(e)}")
        return render_template('home.html', stocks=[], portfolio=None)
