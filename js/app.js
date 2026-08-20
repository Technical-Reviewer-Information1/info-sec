(function () {
  'use strict';
  const $ = id => document.getElementById(id);
  const SUP = { '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹' };
  const sup = n => String(n).split('').map(c => SUP[c] || c).join('');

  /* ===== STEP 1 ===== */
  const TRI = [
    { t: '機密性', d: '許された人だけが情報にアクセスできること。例：暗号化、アクセス制限、パスワード。' },
    { t: '完全性', d: '情報が改ざんされたり壊れたりしていないこと。例：ウイルス対策、電子署名、バックアップ。' },
    { t: '可用性', d: '必要なときにいつでも使えること。例：無停電電源装置、二重化、定期点検。' }
  ];
  const ABC = [
    { k: 'A', t: '悪意のある第三者によるデータの改ざんや盗聴を防ぐために、暗号化して通信をする。', a: '機密性',
      why: '盗聴を防ぐ＝<strong>見られないようにする</strong>ので機密性です。' },
    { k: 'B', t: '大規模な自然災害によるサーバダウンに備えて、無停電電源装置を導入する。', a: '可用性',
      why: '止まらずに<strong>使い続けられる</strong>ようにするので可用性です。' },
    { k: 'C', t: 'データの破壊や改変を防ぐためにウイルス対策ソフトウェアやファイアウォールを導入する。', a: '完全性',
      why: 'データが<strong>壊されたり書きかえられたりしない</strong>ようにするので完全性です。' }
  ];
  const TCH = ['機密性', '完全性', '可用性'];
  let aAns = {};
  function drawTri() {
    $('triBox').innerHTML = TRI.map(t => '<div class="c"><div class="t">' + t.t + '</div><div class="d">' + t.d + '</div></div>').join('');
    $('abcBox').innerHTML = ABC.map((a, i) =>
      '<div style="border:1px solid var(--line);border-radius:3px;padding:10px 12px;margin-bottom:8px">' +
      '<div style="margin-bottom:8px"><strong>' + a.k + '</strong>　' + a.t + '</div>' +
      '<div class="choice4" data-i="' + i + '">' + TCH.map(c =>
        '<button class="btn" data-i="' + i + '" data-c="' + c + '" style="text-align:center">' + c + '</button>').join('') + '</div>' +
      '<div class="note" id="afb' + i + '" hidden style="margin-top:8px"></div></div>').join('');
    $('abcBox').querySelectorAll('button[data-c]').forEach(b => b.addEventListener('click', () => {
      const i = +b.dataset.i, a = ABC[i], ok = b.dataset.c === a.a;
      const row = $('abcBox').querySelector('.choice4[data-i="' + i + '"]');
      row.classList.add('locked');
      [...row.children].forEach(x => { if (x.dataset.c === a.a) x.classList.add('correct'); else if (x === b) x.classList.add('wrong'); });
      const fb = $('afb' + i); fb.hidden = false; fb.className = 'note ' + (ok ? 'ok' : 'ng');
      fb.innerHTML = '<strong>' + a.a + '</strong>　' + a.why;
      aAns[i] = ok;
      const done = Object.keys(aAns).length, right = Object.values(aAns).filter(Boolean).length;
      const n = $('abcNote');
      n.className = 'note ' + (done === ABC.length ? (right === done ? 'ok' : 'warn') : 'info');
      n.innerHTML = done + ' / ' + ABC.length + ' 問（正解 ' + right + ' 問）' +
        (done === ABC.length ? '<br>A＝機密性、B＝可用性、C＝完全性。この組合せが【ア】＝<strong>②</strong>です。' : '');
    }));
    $('abcNote').className = 'note info'; $('abcNote').textContent = '0 / ' + ABC.length + ' 問';
  }

  /* ===== STEP 2 ===== */
  function drawPW() {
    const n = ($('useNum').checked ? 10 : 0) + ($('useLow').checked ? 26 : 0) + ($('useUp').checked ? 26 : 0);
    const L = +$('pwLen').value;
    $('pwLenV').textContent = L;
    $('kindV').textContent = n + ' 種類';
    if (n === 0) { $('patV').textContent = '0'; $('timeV').textContent = '—'; $('pwEq').textContent = '文字の種類を1つ以上選んでください。'; return; }
    const pat = Math.pow(n, L);
    const ex = Math.floor(Math.log10(pat));
    $('patV').innerHTML = (pat / Math.pow(10, ex)).toFixed(2) + ' × 10' + sup(ex) + ' 通り';
    const sec = pat / 1e8;
    let t;
    if (sec < 60) t = sec.toFixed(1) + ' 秒';
    else if (sec < 3600) t = (sec / 60).toFixed(1) + ' 分';
    else if (sec < 86400) t = (sec / 3600).toFixed(1) + ' 時間';
    else if (sec < 3.15e7) t = (sec / 86400).toFixed(1) + ' 日';
    else t = (sec / 3.15e7 < 1e6 ? Math.round(sec / 3.15e7).toLocaleString() + ' 年' : (sec / 3.15e7 / 1e8).toFixed(1) + ' 億年');
    $('timeV').textContent = 'およそ ' + t;
    const parts = [];
    if ($('useNum').checked) parts.push('10');
    if ($('useLow').checked) parts.push('26');
    if ($('useUp').checked) parts.push('26');
    $('pwEq').innerHTML = '（' + parts.join(' ＋ ') + '）' + sup(L) + ' ＝ ' + n + sup(L) + ' 通り';
    const nt = $('pwNote');
    nt.className = 'note ' + (sec > 3.15e9 ? 'ok' : sec > 3.15e7 ? 'warn' : 'ng');
    nt.innerHTML = '文字数を1つ増やすと、パターン数は <strong>' + n + '倍</strong>になります。' +
      (L >= 10 ? '　10文字あれば、総当たりで破るのは現実的に困難です。' : '　文字数が少ないと、短時間で試しつくされてしまいます。') +
      '<br><span class="small">（実際の攻撃はよく使われる語から試すため、辞書に載っている語や誕生日は文字数が多くても危険です）</span>';
  }

  /* ===== STEP 3 ===== */
  const AUTH = [
    { n: '1', t: '利用者がIDとパスワードを入力してログインを試みる。' },
    { n: '2', t: 'サーバが、事前に登録されたスマートフォンに<strong>一度限り有効なパスワード</strong>を送る。' },
    { n: '3', t: '利用者がスマートフォンで受け取ったパスワードを入力する。' },
    { n: '4', t: '2つとも正しければ認証成立。<strong>「知っていること」＋「持っていること」</strong>の両方を確認できた。' }
  ];
  let step = 0;
  function drawAuth() {
    $('authBox').innerHTML = AUTH.map((a, i) =>
      '<div class="s' + (i < step ? ' on' : '') + '"><div class="n">' + a.n + '</div><div class="t">' + (i < step ? a.t : '？') + '</div></div>').join('');
    const n = $('authNote');
    n.className = 'note ' + (step >= 4 ? 'ok' : 'info');
    n.innerHTML = step >= 4
      ? 'パスワードが盗まれても、<strong>登録されたスマートフォンがなければログインできません</strong>。だからセキュリティが強くなります。'
      : step + ' / 4 ステップ。「次のステップ」を押してください。';
    $('authNext').disabled = step >= 4;
  }
  function drawFactor() {
    $('factorTable').innerHTML = '<thead><tr><th>要素</th><th>意味</th><th>例</th></tr></thead><tbody>' +
      '<tr><td>知識情報</td><td>本人だけが<strong>知っていること</strong></td><td>パスワード・暗証番号・秘密の質問</td></tr>' +
      '<tr><td>所持情報</td><td>本人だけが<strong>持っていること</strong></td><td>スマートフォン・ICカード・トークン</td></tr>' +
      '<tr><td>生体情報</td><td>本人自身の<strong>身体的特徴</strong></td><td>指紋・顔・虹彩・声</td></tr></tbody>';
  }

  /* ===== STEP 4 ===== */
  const ATK = [
    { q: '金融機関などからの電子メールを装い、偽サイトに誘導して暗証番号やクレジットカード番号などを不正に取得すること。', a: 'フィッシング' },
    { q: '知らないうちにコンピュータの内部から、個人情報や機密情報を盗み出し、第三者に送信するプログラムのこと。', a: 'スパイウェア' },
    { q: 'Webサイトやメールに記載されたURLを一度クリックしただけで、一方的に契約成立を宣言され、多額の金銭を請求されること。', a: 'ワンクリック詐欺' },
    { q: '肩越しにのぞき見して、パスワードや暗証番号などを入手する行為のこと。', a: 'ショルダーハッキング' }
  ];
  const ACH = ['フィッシング', 'スパイウェア', 'ワンクリック詐欺', 'ショルダーハッキング'];
  let atkAns = {};
  function drawAtk() {
    $('atkBox').innerHTML = ATK.map((a, i) =>
      '<div class="a"><div class="q">' + a.q + '</div>' +
      '<div class="choice4" data-i="' + i + '">' + ACH.map(c =>
        '<button class="btn" data-i="' + i + '" data-c="' + c + '" style="text-align:center">' + c + '</button>').join('') + '</div>' +
      '<div class="note" id="tfb' + i + '" hidden style="margin-top:8px"></div></div>').join('');
    $('atkBox').querySelectorAll('button[data-c]').forEach(b => b.addEventListener('click', () => {
      const i = +b.dataset.i, a = ATK[i], ok = b.dataset.c === a.a;
      const row = $('atkBox').querySelector('.choice4[data-i="' + i + '"]');
      row.classList.add('locked');
      [...row.children].forEach(x => { if (x.dataset.c === a.a) x.classList.add('correct'); else if (x === b) x.classList.add('wrong'); });
      const fb = $('tfb' + i); fb.hidden = false; fb.className = 'note ' + (ok ? 'ok' : 'ng');
      fb.innerHTML = '<strong>' + a.a + '</strong>' +
        (a.a === 'ショルダーハッキング' ? '　人の心理や不注意につけこむ手口を<strong>ソーシャルエンジニアリング</strong>といいます。' : '');
      atkAns[i] = ok;
      const done = Object.keys(atkAns).length, right = Object.values(atkAns).filter(Boolean).length;
      const n = $('atkNote');
      n.className = 'note ' + (done === ATK.length ? (right === done ? 'ok' : 'warn') : 'info');
      n.innerHTML = done + ' / ' + ATK.length + ' 問（正解 ' + right + ' 問）';
    }));
    $('atkNote').className = 'note info'; $('atkNote').textContent = '0 / ' + ATK.length + ' 問';
  }

  function init() {
    drawTri(); drawPW(); drawAuth(); drawFactor(); drawAtk();
    ['useNum', 'useLow', 'useUp'].forEach(i => $(i).addEventListener('change', drawPW));
    $('pwLen').addEventListener('input', drawPW);
    $('pre10').addEventListener('click', () => { $('useNum').checked = $('useLow').checked = $('useUp').checked = true; $('pwLen').value = 10; drawPW(); });
    $('pre8').addEventListener('click', () => { $('useNum').checked = $('useLow').checked = $('useUp').checked = true; $('pwLen').value = 8; drawPW(); });
    $('authNext').addEventListener('click', () => { if (step < 4) { step++; drawAuth(); } });
    $('authReset').addEventListener('click', () => { step = 0; drawAuth(); });
    Quiz.choice('q1Box', 'q1Note', [
      { k: 'ア', q: 'A〜C はそれぞれどの性質を高めるものか。組合せとして最も適当なものは',
        ch: ['A 完全性／B 可用性／C 機密性', 'A 可用性／B 完全性／C 機密性', 'A 機密性／B 可用性／C 完全性', 'A 機密性／B 完全性／C 可用性'],
        a: 2, why: '暗号化＝機密性、無停電電源装置＝可用性、ウイルス対策＝完全性です。' }
    ], '本文の答えは【ア】② です。');
    Quiz.choice('q5Box', 'q5Note', [
      { k: 'オ', q: '10文字、英大文字・小文字と数字が使えるとき、パスワードのパターン数は',
        ch: ['26', '26²', '26¹⁰', '（10＋26）', '（10＋26）²', '（10＋26）¹⁰', '（10＋26＋26）', '（10＋26＋26）²', '（10＋26＋26）¹⁰'],
        a: 8, why: '大文字26＋小文字26＋数字10＝62種類。10文字なので 62¹⁰ ＝（10＋26＋26）¹⁰ 通りです。' },
      { k: 'カ', q: '8文字のサービスと比べると、10文字のパターン数は何倍か',
        ch: ['26', '26²', '26¹⁰', '（10＋26）', '（10＋26）²', '（10＋26）¹⁰', '（10＋26＋26）', '（10＋26＋26）²', '（10＋26＋26）¹⁰'],
        a: 7, why: '62¹⁰ ÷ 62⁸ ＝ 62² ＝（10＋26＋26）² ＝ 3,844倍です。文字数が2つ増えるだけで約3800倍になります。' }
    ], '本文の答えは【オ】⑧　【カ】⑦ です。');
    Quiz.choice('q4Box', 'q4Note', [
      { k: 'エ', q: '二要素認証によってセキュリティが強固になる理由として最も適切なものは',
        ch: ['利用するサイトが正しいサイトであれば、入力したパスワードがスマートフォンに送信されるため', 'パスワードを2回、時間をあけて入力して認証するため', 'IDとパスワードを知っていることに加え、登録されたスマートフォンを持っていることを確認できるため', 'IDとパスワードを知っていることに加え、スマートフォンのGPS機能を使って居場所を特定して認証するため'],
        a: 2, why: '<strong>「知っていること」と「持っていること」という種類の違う2つ</strong>を確認するのが二要素認証です。同じ種類を2回確認しても強くはなりません。' }
    ], '本文の答えは【エ】② です。');
    Quiz.choice('q3Box', 'q3Note', [
      { k: 'ウ', q: 'フィッシングに関する記述として最も適切なものは',
        ch: ['知らないうちにコンピュータの内部から、個人情報や機密情報を盗み出し、第三者に送信するプログラムのこと', '金融機関などからの電子メールを装い、偽サイトに誘導して暗証番号やクレジットカード番号などを不正に取得すること', 'Webサイトやメールに記載されたURLを一度クリックしただけで、一方的にサービスへの契約成立を宣言され、多額の金銭を請求されること', '肩越しにのぞき見して、パスワードや暗証番号などを入手する行為のこと'],
        a: 1, why: '⓪はスパイウェア、②はワンクリック詐欺、③はショルダーハッキングの説明です。' }
    ], '本文の答えは【ウ】① です。');
    Quiz.choice('q2Box', 'q2Note', [
      { k: 'イ', q: '情報セキュリティに関する記述として<strong>適当でない</strong>ものは',
        ch: ['フィルタリングサービスを導入することにより、有害なサイトへのアクセスを制限できたり、個人情報の漏洩を防ぐことができたりする', '内部ネットワークとインターネットとの間にファイアウォールを設置することで、外部からの不正なアクセスや機密情報の漏洩などを防ぐことができる', 'ウイルス対策ソフトウェアを導入し、定義ファイルを常に最新のものに保つことで、マルウェアに感染することはない', '人間の心理的な隙や不注意につけ込み、不正にパスワードや機密情報が盗まれることもある'],
        a: 2, why: '定義ファイルを最新にしても、<strong>新しい未知のマルウェアには対応できません</strong>。「絶対に感染しない」とは言えません。' }
    ], '本文の答えは【イ】② です。');
    Quiz.choice('q6Box', 'q6Note', [
      { k: 'キ', q: '会員登録において、情報セキュリティの観点に基づいた行動として最も適当なものは',
        ch: ['会員登録サイトにアクセスする際は、確実にインターネットに接続できるように、ショッピングモールなどの公衆無線LANを利用する', '会員登録を行う際は、個人のパソコンではなく、学校や図書館などに設置されている共有パソコンを利用する', '会員情報を入力する際は、自分の周囲で他人が登録画面をのぞき込んでいないか、注意を払いながら入力する', '会員登録が終わった後は、登録したユーザIDやパスワードを失念しないように紙に印刷し、目立つ場所に掲示する'],
        a: 2, why: '<strong>ショルダーハッキング</strong>への対策です。⓪の公衆無線LANは盗聴の危険、①の共有パソコンは入力内容が残る危険、③は誰でも見られる状態になり最も危険です。' }
    ], '本文の答えは【キ】② です。');
    window.Terms.glossary($('glossBox'), ['情報セキュリティ', '機密性', '完全性', '可用性', '二要素認証', 'フィッシング', 'ソーシャルエンジニアリング', 'ファイアウォール', 'マルウェア']);
    window.Terms.attach();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
