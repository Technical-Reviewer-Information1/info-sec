import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import re

def calculate_password_strength(password):
    """パスワード強度を計算する関数"""
    score = 0
    feedback = []
    
    if len(password) >= 8:
        score += 25
    else:
        feedback.append("8文字以上にしてください")
    
    if re.search(r'[a-z]', password) and re.search(r'[A-Z]', password):
        score += 25
    else:
        feedback.append("大文字と小文字を含めてください")
    
    if re.search(r'\d', password):
        score += 25
    else:
        feedback.append("数字を含めてください")
    
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 25
    else:
        feedback.append("記号を含めてください")
    
    # よくあるパターンをチェック
    common_patterns = ['123', 'abc', 'password', 'admin', 'qwerty']
    if any(pattern in password.lower() for pattern in common_patterns):
        score -= 20
        feedback.append("よくあるパターンは避けてください")
    
    return min(100, max(0, score)), feedback

def create_password_strength_chart(score):
    """パスワード強度を可視化するチャート"""
    if score < 30:
        color = 'red'
        strength = '弱い'
    elif score < 70:
        color = 'orange'
        strength = '普通'
    else:
        color = 'green'
        strength = '強力'
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = score,
        title = {'text': f"パスワード強度: {strength}"},
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 30], 'color': "lightgray"},
                {'range': [30, 70], 'color': "gray"},
                {'range': [70, 100], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=300)
    return fig

def create_security_threats_chart():
    """セキュリティ脅威の統計チャート"""
    threats_data = {
        '脅威の種類': ['フィッシング詐欺', 'マルウェア', 'パスワード攻撃', 'ソーシャルエンジニアリング', 'データ漏洩'],
        '発生頻度(%)': [35, 28, 20, 12, 5]
    }
    
    df = pd.DataFrame(threats_data)
    
    fig = px.pie(df, values='発生頻度(%)', names='脅威の種類',
                 title='主なサイバーセキュリティ脅威の分布',
                 color_discrete_sequence=px.colors.qualitative.Set3)
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)
    return fig

def main():
    st.set_page_config(
        page_title="情報セキュリティ",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    st.title("🛡️ 情報セキュリティ")
    st.caption("Created by Dit-Lab.(Daiki ITO)")
    st.caption("Supported by Tomoaki ATSUMI")
    
    # セッション状態の初期化
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    
    # ステップナビゲーション
    steps = ['はじめに', 'ログイン認証', 'メールチェック', 'パスワード作成', 'まとめ']
    
    # プログレスバー
    progress = (st.session_state.step - 1) / (len(steps) - 1)
    st.progress(progress)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    cols = [col1, col2, col3, col4, col5]
    
    for i, (step_name, col) in enumerate(zip(steps, cols)):
        if i + 1 == st.session_state.step:
            col.write(f"**{i+1}. {step_name}** 📍")
        else:
            col.write(f"{i+1}. {step_name}")
    
    st.markdown("---")
    
    # ステップ1: はじめに
    if st.session_state.step == 1:
        st.header("ステップ1: はじめに - デジタル世界を守る「3つの盾」")
        
        st.markdown("""
        私たちの便利なデジタルライフは、常に様々な危険にさらされています。
        情報セキュリティとは、あなたの大切な情報を守るための「防御術」です。
        
        この防御術には、基本となる「3つの盾」があります。まずは、この盾について知りましょう！
        """)
        
        # 3つの盾の紹介
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("""
            **【機密性 - Confidentiality】**
            
            🔐 許可された人だけが見れる盾
            
            • IDとパスワードによる認証
            • データの暗号化
            • アクセス権限の管理
            """)
        
        with col2:
            st.success("""
            **【完全性 - Integrity】**
            
            ✅ データが改ざんされない盾
            
            • デジタル署名
            • ハッシュ値による検証
            • バックアップとバージョン管理
            """)
        
        with col3:
            st.warning("""
            **【可用性 - Availability】**
            
            🔄 いつでも使えるようにする盾
            
            • システムの冗長化
            • 定期的なバックアップ
            • 災害復旧対策
            """)
        
        # セキュリティ脅威の可視化
        st.subheader("🚨 現在のサイバーセキュリティ脅威")
        fig = create_security_threats_chart()
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        さあ、これから始まるシミュレーションで、この盾をどう使っていくか体験してみましょう！
        """)
        
        if st.button("次のステップへ →", key="step1_next"):
            st.session_state.step = 2
            st.rerun()
    
    # ステップ2: ログイン認証
    elif st.session_state.step == 2:
        st.header("ステップ2: Case 1 - ネット銀行へのログイン、最強の鍵はどれ？")
        
        st.markdown("""
        🏦 **シナリオ**: あなたのネット銀行口座を守るため、ログイン方法を選びます。
        最も安全な方法はどれでしょうか？
        """)
        
        # 認証方法の選択
        auth_choice = st.radio(
            "最も安全なログイン方法は？",
            [
                "A: IDとパスワードだけでログイン",
                "B: 指紋認証だけでログイン", 
                "C: IDとパスワードを入力した後、スマホのSMSに届く確認コードも入力する"
            ],
            key="auth_choice"
        )
        
        if auth_choice:
            st.session_state.answers['auth'] = auth_choice
            
            st.markdown("---")
            
            if auth_choice == "C: IDとパスワードを入力した後、スマホのSMSに届く確認コードも入力する":
                st.success("🎉 正解です！")
                st.markdown("""
                **これは二要素認証（2FA）と呼ばれ、非常に強力なセキュリティです。**
                
                📱 **二要素認証の仕組み**:
                • **知識認証**（あなたが知っているもの）: パスワード
                • **所有物認証**（あなたが持っているもの）: スマートフォン
                
                このように、種類の違う「カギ」を2つ組み合わせることで、
                不正ログインを格段に防ぎやすくなります。
                
                **🛡️ 機密性の盾** を最大限に活用した方法です！
                """)
            else:
                st.error("❌ 不正解です。")
                if "A:" in auth_choice:
                    st.markdown("""
                    **パスワードだけでは不十分です。**
                    パスワードが漏洩した場合、簡単に不正アクセスされてしまいます。
                    """)
                else:
                    st.markdown("""
                    **指紋認証だけでも不十分です。**
                    指紋データが複製される可能性もあり、単一要素では脆弱です。
                    """)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← 前のステップへ", key="step2_prev"):
                st.session_state.step = 1
                st.rerun()
        with col2:
            if st.button("次のステップへ →", key="step2_next"):
                st.session_state.step = 3
                st.rerun()
    
    # ステップ3: メールチェック
    elif st.session_state.step == 3:
        st.header("ステップ3: Case 2 - 届いたメールは本物？それとも罠？")
        
        st.markdown("""
        📧 **シナリオ**: あなたが利用しているショッピングサイト「MarketPlace」から、
        こんなメールが届きました。
        """)
        
        # 疑似フィッシングメールの表示
        with st.container():
            st.markdown("""
            <div style="border: 2px solid #ff4444; padding: 20px; background-color: #fff5f5; border-radius: 10px;">
            <h4>⚠️ 緊急：MarketPlace アカウント停止のお知らせ</h4>
            <hr>
            <p><strong>送信者:</strong> security@market-place-official.com</p>
            <p><strong>件名:</strong> 【緊急】アカウント確認が必要です</p>
            <hr>
            <p>お客様のMarketPlaceアカウントで不審なアクティビティが検出されました。</p>
            <p><strong>24時間以内</strong>にアカウント情報を確認しないと、アカウントが永久停止されます。</p>
            <p>今すぐ下記リンクからログインして確認してください：</p>
            <p><a href="#" style="color: blue;">https://marketplace-security-check.net/login</a></p>
            <p>※このメールは自動送信されています</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### あなたならどうしますか？")
        
        email_choice = st.selectbox(
            "行動を選択してください：",
            [
                "選択してください",
                "大変だ！急いでリンクをクリックして、パスワードを再入力する。",
                "怪しい…。送信元アドレスを確認し、このメールは無視して公式サイトからログインする。"
            ],
            key="email_choice"
        )
        
        if email_choice and email_choice != "選択してください":
            st.session_state.answers['email'] = email_choice
            
            st.markdown("---")
            
            if "怪しい" in email_choice:
                st.success("🎉 正解です！素晴らしい判断力です！")
                st.markdown("""
                **これは、偽サイトに誘導してIDやパスワードを盗み取る**
                **フィッシング詐欺の典型的な手口です。**
                
                🕵️ **見破るポイント**:
                • 送信元アドレス: `market-place-official.com` (本物は `marketplace.com`)
                • 緊急性を煽る文章
                • 不自然なリンク先: `marketplace-security-check.net`
                • 文法やスペルのミス
                
                **🛡️ 機密性の盾** を守る正しい行動です！
                
                💡 **対処法**:
                1. 怪しいメールのリンクは絶対にクリックしない
                2. 公式サイトに直接アクセスして確認
                3. 企業の公式サポートに問い合わせ
                """)
            else:
                st.error("❌ 危険です！")
                st.markdown("""
                **あなたは今、フィッシング詐欺の罠に引っかかりました。**
                
                偽のウェブサイトにIDとパスワードを入力することで、
                あなたの認証情報が悪用される可能性があります。
                
                🚨 **実際に起こりうる被害**:
                • アカウントの乗っ取り
                • 個人情報の漏洩  
                • 金銭的被害
                • 他のサービスへの不正アクセス
                """)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← 前のステップへ", key="step3_prev"):
                st.session_state.step = 2
                st.rerun()
        with col2:
            if st.button("次のステップへ →", key="step3_next"):
                st.session_state.step = 4
                st.rerun()
    
    # ステップ4: パスワード作成
    elif st.session_state.step == 4:
        st.header("ステップ4: Case 3 - 新しいサービスのパスワード、どれにする？")
        
        st.markdown("""
        🔐 **シナリオ**: 新しいSNSに登録します。安全なパスワードを設定してください。
        """)
        
        # パスワード入力
        password = st.text_input("パスワードを入力してください:", type="password", key="password_input")
        
        if password:
            # パスワード強度計算
            score, feedback = calculate_password_strength(password)
            
            # 強度メーターの表示
            col1, col2 = st.columns([2, 1])
            
            with col1:
                fig = create_password_strength_chart(score)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### 📋 チェックリスト")
                
                # チェックボックス
                check1 = st.checkbox("8文字以上にしましたか？", value=len(password) >= 8, disabled=True)
                check2 = st.checkbox("大文字、小文字、数字、記号を混ぜましたか？", 
                                   value=bool(re.search(r'[a-z]', password) and 
                                           re.search(r'[A-Z]', password) and 
                                           re.search(r'\d', password) and 
                                           re.search(r'[!@#$%^&*(),.?":{}|<>]', password)), 
                                   disabled=True)
                check3 = st.checkbox("名前や誕生日など、推測されやすい文字列を避けていますか？",
                                   value=not any(pattern in password.lower() for pattern in ['123', 'abc', 'password', 'admin', 'qwerty']),
                                   disabled=True)
            
            # フィードバック表示
            if feedback:
                st.warning("💡 改善提案:")
                for tip in feedback:
                    st.write(f"• {tip}")
            
            if score >= 70:
                st.success("""
                🎉 **強力なパスワードです！**
                
                あなたのパスワードは **🛡️ 機密性の盾** を強化します！
                """)
        
        st.markdown("""
        ---
        ### 📚 パスワードセキュリティの重要性
        
        パスワードは、文字数が1文字増えるだけで、解読される確率が何十倍も低くなります。
        
        **「長く」「複雑に」「推測されにくく」** が、あなたのデジタルライフを守る合言葉です。
        """)
        
        # パスワード解読時間の可視化
        if password:
            length = len(password)
            has_upper = bool(re.search(r'[A-Z]', password))
            has_lower = bool(re.search(r'[a-z]', password))
            has_digit = bool(re.search(r'\d', password))
            has_symbol = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
            
            char_space = 0
            if has_lower: char_space += 26
            if has_upper: char_space += 26  
            if has_digit: char_space += 10
            if has_symbol: char_space += 32
            
            if char_space > 0 and length > 0:
                combinations = char_space ** length
                # 1秒で10億回試行と仮定
                seconds = combinations / 2 / 1_000_000_000
                
                if seconds < 60:
                    time_str = f"{seconds:.1f}秒"
                elif seconds < 3600:
                    time_str = f"{seconds/60:.1f}分"
                elif seconds < 86400:
                    time_str = f"{seconds/3600:.1f}時間"
                elif seconds < 31536000:
                    time_str = f"{seconds/86400:.1f}日"
                else:
                    time_str = f"{seconds/31536000:.1f}年"
                
                st.info(f"🕐 このパスワードを総当たりで解読するのに必要な平均時間: **{time_str}**")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← 前のステップへ", key="step4_prev"):
                st.session_state.step = 3
                st.rerun()
        with col2:
            if st.button("次のステップへ →", key="step4_next"):
                st.session_state.step = 5
                st.rerun()
    
    # ステップ5: まとめ
    elif st.session_state.step == 5:
        st.header("ステップ5: 今日のサバイバルと防御術の振り返り")
        
        st.markdown("""
        🎓 **お疲れ様でした！**
        
        今日あなたが体験した行動は、情報セキュリティの「3つの盾」と深く関わっています。
        """)
        
        # 3つの盾と今日の学習の関連付け
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("""
            **🔐 機密性 (Confidentiality)**
            
            **今日の実践:**
            • 二要素認証の選択
            • フィッシング詐欺の回避
            • 強力なパスワードの作成
            
            **効果:**
            許可されていない人からの
            情報アクセスを防ぐ
            """)
        
        with col2:
            st.success("""
            **✅ 完全性 (Integrity)**
            
            **関連する対策:**
            • ウイルス対策ソフトの更新
            • デジタル署名の確認
            • 定期的なシステム更新
            
            **効果:**
            データの改ざんや
            破壊から守る
            """)
        
        with col3:
            st.warning("""
            **🔄 可用性 (Availability)**
            
            **関連する対策:**
            • 定期的なバックアップ
            • 災害復旧計画
            • システムの冗長化
            
            **効果:**
            いつでもサービスを
            利用できる状態を維持
            """)
        
        # 学習成果の可視化
        st.subheader("📊 あなたの学習成果")
        
        # 答えの分析
        correct_answers = 0
        total_questions = 0
        
        if 'auth' in st.session_state.answers:
            total_questions += 1
            if "C:" in st.session_state.answers['auth']:
                correct_answers += 1
        
        if 'email' in st.session_state.answers:
            total_questions += 1
            if "怪しい" in st.session_state.answers['email']:
                correct_answers += 1
        
        if total_questions > 0:
            score_percentage = (correct_answers / total_questions) * 100
            
            # スコア表示
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = score_percentage,
                title = {'text': "セキュリティ理解度"},
                domain = {'x': [0, 1], 'y': [0, 1]},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkgreen" if score_percentage >= 80 else "orange" if score_percentage >= 60 else "red"},
                    'steps': [
                        {'range': [0, 60], 'color': "lightgray"},
                        {'range': [60, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "lightgreen"}
                    ]
                }
            ))
            
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        # 今後のアクションプラン
        st.subheader("🚀 今後のアクションプラン")
        
        recommendations = [
            "📱 お使いのアカウントで二要素認証を有効にする",
            "🔄 定期的にパスワードを変更・管理する", 
            "📧 不審なメールやメッセージに注意を払う",
            "💾 重要なデータの定期バックアップを取る",
            "🛡️ ウイルス対策ソフトを常に最新に保つ",
            "📚 セキュリティに関する知識を継続的に学ぶ"
        ]
        
        for rec in recommendations:
            st.write(f"• {rec}")
        
        st.success("""
        🎉 **これらの知識を身につけたあなたは、もう立派なデジタルサバイバーです！**
        
        継続的な学習と実践で、より安全なデジタルライフを送りましょう。
        """)
        
        # 最終アクション
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← 前のステップへ", key="step5_prev"):
                st.session_state.step = 4
                st.rerun()
        with col2:
            if st.button("🔄 最初からやり直す", key="restart"):
                # セッション状態をリセット
                st.session_state.step = 1
                st.session_state.answers = {}
                st.rerun()

if __name__ == "__main__":
    main()