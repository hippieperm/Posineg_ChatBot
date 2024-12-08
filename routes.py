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
            'stocks': [],  # 주식 데이터 리스트
            'portfolio': None  # 포트폴리오 정보
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

# 마켓 페이지 라우트
@main.route('/market')
@login_required  # 로그인한 사용자만 접근 가능
def market():
    """마켓 페이지를 표시합니다."""
    return render_template('market.html')

# 포트폴리오 계산 헬퍼 함수
def calculate_portfolio_data(user):
    """사용자의 포트폴리오 정보를 계산합니다."""
    try:
        # 사용자 보유 주식 데이터를 가져옴
        holdings = StockHolding.query.filter_by(user_id=user.id).all()
        
        total_assets = user.cash if user.cash is not None else 0  # 총 자산 (현금 포함)
        invested_amount = 0  # 투자된 금액
        holdings_data = []  # 보유 주식 데이터

        # 각 보유 주식에 대해 데이터 처리
        for holding in holdings:
            holding_dict = holding.to_dict()  # 주식 정보 딕셔너리로 변환
            total_value = holding_dict['total_value']  # 총 가치
            avg_price = holding_dict['avg_price']  # 평균 가격
            quantity = holding_dict['quantity']  # 보유 수량

            # 보유 주식 정보 추가
            holdings_data.append({
                'stock_name': holding_dict['stock_name'],
                'quantity': quantity,
                'avg_price': avg_price,
                'current_price': holding_dict['current_price'],
                'total_value': total_value,
                'return_rate': holding_dict['return_rate'],
                'profit_loss': holding_dict['profit_loss']
            })

            total_assets += total_value  # 총 자산 갱신
            invested_amount += avg_price * quantity  # 투자 금액 갱신

        # 총 수익률 계산
        total_return_rate = ((total_assets - 10000000) / 10000000) * 100 if total_assets > 0 else 0

        return {
            'holdings': holdings_data,
            'total_assets': total_assets,
            'invested_amount': invested_amount,
            'total_return_rate': total_return_rate,
            'cash': user.cash  # 사용자의 현금
        }
    except Exception as e:
        print(f"Error calculating portfolio data: {str(e)}")
        return {
            'holdings': [],
            'total_assets': user.cash if user.cash is not None else 0,
            'invested_amount': 0,
            'total_return_rate': 0,
            'cash': user.cash if user.cash is not None else 0
        }
