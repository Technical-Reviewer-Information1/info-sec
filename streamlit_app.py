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

def create_security_threats_ranking():
    """IPA情報セキュリティ10大脅威 2024年版 ランキング表示"""
    
    # 組織向け脅威ランキング（IPA 2024年版）
    org_threats = [
        "ランサムウェア",
        "サプライチェーンの弱点を悪用した攻撃",
        "内部不正による情報漏えい",
        "標的型攻撃による機密情報の窃取", 
        "修正プログラムの公開前を狙う攻撃（ゼロデイ攻撃）",
        "不注意による情報漏えい等の被害",
        "脆弱性対策情報の公開に伴い公開前よりリスクが増加する脆弱性（整理番号7）",
        "ビジネスメール詐欺による金銭被害",
        "テレワーク等のニューノーマルな働き方を狙った攻撃",
        "サイバー犯罪のビジネス化（アンダーグラウンドサービス）"
    ]
    
    # 個人向け脅威（順位付けなし、アルファベット順）
    individual_threats = [
        "インターネット上のサービスからの個人情報の窃取",
        "インターネット上のサービスへの不正ログイン",
        "クレジットカード情報の不正利用",
        "スマホ決済の不正利用",
        "偽警告によるインターネット詐欺",
        "ネット上の誹謗・中傷・デマ",
        "フィッシングによる個人情報等の詐取",
        "悪意のあるスマートフォンアプリ",
        "メール・SMS等を使った脅迫・詐欺の手口による金銭要求",
        "ワンクリック請求等の不当請求による金銭被害"
    ]
    
    return org_threats, individual_threats

def main():
    st.set_page_config(
        page_title="情報セキュリティ",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    st.title("情報セキュリティ（pp.220-224）")
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
            st.markdown("""
            <div style="background-color: #d1ecf1; border: 2px solid #bee5eb; padding: 20px; border-radius: 10px; color: #0c5460;">
            <h4 style="color: #0c5460; margin-top: 0;">🔐 機密性 - Confidentiality</h4>
            <h5 style="color: #0c5460;">許可された人だけが見れる盾</h5>
            <ul style="color: #0c5460; font-size: 15px; line-height: 1.6;">
            <li>IDとパスワードによる認証</li>
            <li>データの暗号化</li>
            <li>アクセス権限の管理</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background-color: #d4edda; border: 2px solid #c3e6cb; padding: 20px; border-radius: 10px; color: #155724;">
            <h4 style="color: #155724; margin-top: 0;">✅ 完全性 - Integrity</h4>
            <h5 style="color: #155724;">データが改ざんされない盾</h5>
            <ul style="color: #155724; font-size: 15px; line-height: 1.6;">
            <li>デジタル署名</li>
            <li>ハッシュ値による検証</li>
            <li>バックアップとバージョン管理</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background-color: #fff3cd; border: 2px solid #ffeaa7; padding: 20px; border-radius: 10px; color: #856404;">
            <h4 style="color: #856404; margin-top: 0;">🔄 可用性 - Availability</h4>
            <h5 style="color: #856404;">いつでも使えるようにする盾</h5>
            <ul style="color: #856404; font-size: 15px; line-height: 1.6;">
            <li>システムの冗長化</li>
            <li>定期的なバックアップ</li>
            <li>災害復旧対策</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # セキュリティ脅威のランキング表示
        st.subheader("🚨 IPA情報セキュリティ10大脅威 2024年版")
        
        org_threats, individual_threats = create_security_threats_ranking()
        
        # タブで組織向けと個人向けを分離
        tab1, tab2 = st.tabs(["🏢 組織向け脅威", "👤 個人向け脅威"])
        
        with tab1:
            st.markdown("### 組織における脅威ランキング")
            st.markdown("*IPAによる投票結果に基づく順位*")
            
            for i, threat in enumerate(org_threats, 1):
                if i <= 3:
                    # トップ3は強調表示
                    medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
                    bg_color = "#ffebee" if i == 1 else "#fff3e0" if i == 2 else "#fffde7"
                    border_color = "#e57373" if i == 1 else "#ffb74d" if i == 2 else "#fff176"
                    st.markdown(f"""
                    <div style="background-color: {bg_color}; 
                                padding: 12px; margin: 5px 0; border-radius: 8px; 
                                border-left: 4px solid {border_color};">
                    <h4 style="margin: 0; color: #2c3e50;">{medal} 第{i}位: {threat}</h4>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"**{i}位**: {threat}")
        
        with tab2:
            st.markdown("### 個人における脅威一覧")
            st.markdown("*2024年版では個人向け脅威は順位付けなし（アルファベット順）*")
            
            # 2列で表示
            col1, col2 = st.columns(2)
            
            for i, threat in enumerate(individual_threats):
                target_col = col1 if i < 5 else col2
                with target_col:
                    st.markdown(f"• {threat}")
        
        st.markdown("---")
        st.caption("📊 出典: IPA（独立行政法人情報処理推進機構）情報セキュリティ10大脅威 2024年版")
        st.caption("🔗 参考URL: https://www.ipa.go.jp/security/10threats/10threats2024.html")
        st.caption("⚠️ 組織向けは投票による順位付き、個人向けは順位なしで掲載")
        
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
        
        # 回答ボタンを追加
        answer_submitted = False
        if auth_choice and 'auth_answer_submitted' not in st.session_state:
            if st.button("回答する", key="submit_auth"):
                st.session_state.answers['auth'] = auth_choice
                st.session_state.auth_answer_submitted = True
                answer_submitted = True
                st.rerun()
        elif 'auth_answer_submitted' in st.session_state:
            answer_submitted = True
            
        if answer_submitted:
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
            <div style="border: 3px solid #dc3545; padding: 25px; background-color: #f8f9fa; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            <h3 style="color: #dc3545; margin-top: 0;">⚠️ 緊急：MarketPlace アカウント停止のお知らせ</h3>
            <hr style="border-color: #dc3545;">
            <p style="color: #212529; font-size: 16px; margin: 10px 0;"><strong>送信者:</strong> <span style="color: #dc3545;">security@market-place-official.com</span></p>
            <p style="color: #212529; font-size: 16px; margin: 10px 0;"><strong>件名:</strong> 【緊急】アカウント確認が必要です</p>
            <hr style="border-color: #dc3545;">
            <p style="color: #212529; font-size: 16px; line-height: 1.6; margin: 15px 0;">お客様のMarketPlaceアカウントで不審なアクティビティが検出されました。</p>
            <p style="color: #212529; font-size: 16px; line-height: 1.6; margin: 15px 0;"><strong style="color: #dc3545; font-size: 18px;">24時間以内</strong>にアカウント情報を確認しないと、アカウントが永久停止されます。</p>
            <p style="color: #212529; font-size: 16px; line-height: 1.6; margin: 15px 0;">今すぐ下記リンクからログインして確認してください：</p>
            <p style="margin: 20px 0;"><a href="#" style="color: #007bff; font-size: 16px; text-decoration: underline; background-color: #e3f2fd; padding: 8px 12px; border-radius: 4px; display: inline-block;">https://marketplace-security-check.net/login</a></p>
            <p style="color: #6c757d; font-size: 14px; font-style: italic; margin: 15px 0;">※このメールは自動送信されています</p>
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
        
        # 回答ボタンを追加
        email_answer_submitted = False
        if email_choice and email_choice != "選択してください" and 'email_answer_submitted' not in st.session_state:
            if st.button("回答する", key="submit_email"):
                st.session_state.answers['email'] = email_choice
                st.session_state.email_answer_submitted = True
                email_answer_submitted = True
                st.rerun()
        elif 'email_answer_submitted' in st.session_state:
            email_answer_submitted = True
            
        if email_answer_submitted:
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
                st.checkbox("8文字以上にしましたか？", value=len(password) >= 8, disabled=True)
                st.checkbox("大文字、小文字、数字、記号を混ぜましたか？", 
                           value=bool(re.search(r'[a-z]', password) and 
                                   re.search(r'[A-Z]', password) and 
                                   re.search(r'\d', password) and 
                                   re.search(r'[!@#$%^&*(),.?":{}|<>]', password)), 
                           disabled=True)
                st.checkbox("名前や誕生日など、推測されやすい文字列を避けていますか？",
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
        
        # パスワード解読時間の可視化（複数のハードウェア構成）
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
                
                # 様々な攻撃手法とハードウェア構成
                attack_methods = {
                    "個人PC（CPU）": {
                        "speed": 1_000_000,  # 1秒で100万回
                        "description": "Intel Core i7-13700K（約5万円）",
                        "cost": "5万円",
                        "accessibility": "🟢 個人レベル"
                    },
                    "ゲーミングPC（GPU）": {
                        "speed": 50_000_000,  # 1秒で5000万回
                        "description": "NVIDIA RTX 4070（約10万円）",
                        "cost": "15万円",
                        "accessibility": "🟡 愛好家レベル"
                    },
                    "高性能GPU": {
                        "speed": 100_000_000,  # 1秒で1億回
                        "description": "NVIDIA RTX 4090（約25万円）",
                        "cost": "30万円",
                        "accessibility": "🟡 プロレベル"
                    },
                    "マイニングリグ": {
                        "speed": 500_000_000,  # 1秒で5億回
                        "description": "RTX 4090 × 4台構成",
                        "cost": "120万円",
                        "accessibility": "🟠 組織レベル"
                    },
                    "専用クラスター": {
                        "speed": 2_000_000_000,  # 1秒で20億回
                        "description": "GPU 8台 + 専用サーバー",
                        "cost": "500万円",
                        "accessibility": "🔴 犯罪組織レベル"
                    },
                    "クラウドクラスター": {
                        "speed": 10_000_000_000,  # 1秒で100億回
                        "description": "AWS/Azure GPU大規模構成",
                        "cost": "時間課金（数万円/時間）",
                        "accessibility": "🔴 国家レベル"
                    }
                }
                
                st.subheader("🖥️ ハードウェア別 解読時間比較")
                
                # テーブル形式で表示
                attack_data = []
                for method_name, method_info in attack_methods.items():
                    seconds = combinations / 2 / method_info["speed"]  # 平均時間
                    
                    if seconds < 1:
                        time_str = f"{seconds*1000:.0f}ミリ秒"
                    elif seconds < 60:
                        time_str = f"{seconds:.1f}秒"
                    elif seconds < 3600:
                        time_str = f"{seconds/60:.1f}分"
                    elif seconds < 86400:
                        time_str = f"{seconds/3600:.1f}時間"
                    elif seconds < 31536000:
                        time_str = f"{seconds/86400:.0f}日"
                    elif seconds < 31536000000:
                        time_str = f"{seconds/31536000:.0f}年"
                    else:
                        time_str = "数千年以上"
                    
                    attack_data.append({
                        "ハードウェア構成": method_name,
                        "解読時間": time_str,
                        "機材詳細": method_info["description"],
                        "概算コスト": method_info["cost"],
                        "アクセス難易度": method_info["accessibility"]
                    })
                
                # DataFrameとして表示
                df_attacks = pd.DataFrame(attack_data)
                st.dataframe(df_attacks, use_container_width=True, hide_index=True)
                
                st.markdown("""
                ---
                ### ⚠️ 現実的な脅威について
                
                **実際の攻撃で使われる手法:**
                - **辞書攻撃**: よくあるパスワードリスト（rockyou.txt等）を使用 → 数秒〜数分
                - **マスクアタック**: パターンを指定した総当たり → 数時間〜数日
                - **ハイブリッド攻撃**: 辞書+ルールベース変換 → 数分〜数時間
                - **レインボーテーブル**: 事前計算済みハッシュ表 → 瞬時〜数分
                - **ソーシャルエンジニアリング**: 心理的手法で直接情報入手 → 瞬時
                - **データ漏洩**: 他サイトから流出したパスワードを試行 → 数秒
                
                **現実的な防御戦略:**
                """)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("""
                    **強度レベル1（基本）:**
                    - 💪 12文字以上の長さ
                    - 🔀 文字種類の混合
                    - 🚫 辞書単語を避ける
                    - 🔄 サイト別に異なるパスワード
                    """)
                
                with col2:
                    st.markdown("""
                    **強度レベル2（推奨）:**
                    - 🛡️ パスワードマネージャー使用
                    - 📱 二要素認証の有効化
                    - 🔄 定期的な変更（重要サービス）
                    - 📧 セキュリティ通知の監視
                    """)
                
                st.info("""
                **💡 実践的なパスワード作成例:**
                - ❌ 弱い例: `password123`, `yamada2024`
                - ✅ 強い例: `Coffee#Morning@2024!`, `MyDog&3Cats=Family`
                - 🏆 最強例: パスワードマネージャーで生成された32文字ランダム文字列
                """)
                
                st.warning("""
                **注意**: この情報は防御目的での教育用です。
                実際のパスワード攻撃は違法行為であり、絶対に行ってはいけません。
                """)
        
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
            st.markdown("""
            <div style="background-color: #d1ecf1; border: 2px solid #bee5eb; padding: 20px; border-radius: 10px; color: #0c5460;">
            <h4 style="color: #0c5460; margin-top: 0;">🔐 機密性 (Confidentiality)</h4>
            <h5 style="color: #0c5460;">今日の実践:</h5>
            <ul style="color: #0c5460; font-size: 15px; line-height: 1.6;">
            <li>二要素認証の選択</li>
            <li>フィッシング詐欺の回避</li>
            <li>強力なパスワードの作成</li>
            </ul>
            <h5 style="color: #0c5460;">効果:</h5>
            <p style="color: #0c5460; font-size: 15px;">許可されていない人からの情報アクセスを防ぐ</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background-color: #d4edda; border: 2px solid #c3e6cb; padding: 20px; border-radius: 10px; color: #155724;">
            <h4 style="color: #155724; margin-top: 0;">✅ 完全性 (Integrity)</h4>
            <h5 style="color: #155724;">関連する対策:</h5>
            <ul style="color: #155724; font-size: 15px; line-height: 1.6;">
            <li>ウイルス対策ソフトの更新</li>
            <li>デジタル署名の確認</li>
            <li>定期的なシステム更新</li>
            </ul>
            <h5 style="color: #155724;">効果:</h5>
            <p style="color: #155724; font-size: 15px;">データの改ざんや破壊から守る</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background-color: #fff3cd; border: 2px solid #ffeaa7; padding: 20px; border-radius: 10px; color: #856404;">
            <h4 style="color: #856404; margin-top: 0;">🔄 可用性 (Availability)</h4>
            <h5 style="color: #856404;">関連する対策:</h5>
            <ul style="color: #856404; font-size: 15px; line-height: 1.6;">
            <li>定期的なバックアップ</li>
            <li>災害復旧計画</li>
            <li>システムの冗長化</li>
            </ul>
            <h5 style="color: #856404;">効果:</h5>
            <p style="color: #856404; font-size: 15px;">いつでもサービスを利用できる状態を維持</p>
            </div>
            """, unsafe_allow_html=True)
        
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
