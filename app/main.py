from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from app.routers import hobby

app = FastAPI(title="my-hobby")

app.include_router(hobby.router, prefix="/api")


@app.get("/", response_class=HTMLResponse)
async def index():
    return """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>my-hobby</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f5f5f5; }
        h1 { text-align: center; padding: 24px; color: #333; }
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            grid-template-rows: 1fr 1fr;
            gap: 12px;
            max-width: 600px;
            height: 60vh;
            margin: 0 auto;
            padding: 0 16px;
        }
        .cell {
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 16px;
            font-size: 1.4rem;
            font-weight: 600;
            color: #fff;
            cursor: pointer;
            transition: transform 0.15s, opacity 0.15s;
        }
        .cell:hover { transform: scale(1.03); }
        .cell[data-id="1"] { background: #4CAF50; }
        .cell[data-id="2"] { background: #2196F3; }
        .cell[data-id="3"] { background: #FF9800; }
        .cell[data-id="4"] { background: #9C27B0; }
        .cell.locked {
            opacity: 0.5;
            cursor: default;
            font-size: 1.1rem;
        }
        .cell.locked:hover { transform: none; }
        .cell.proceed {
            border: 3px dashed #fff;
            font-size: 1.1rem;
        }
        #result {
            max-width: 600px;
            margin: 24px auto;
            padding: 0 16px;
            display: none;
        }
        #result h2 { margin-bottom: 12px; color: #333; }
        #result ul { list-style: none; }
        #result li {
            background: #fff;
            padding: 16px;
            margin-bottom: 8px;
            border-radius: 10px;
            font-size: 1.1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        #result li.more-btn {
            background: #eee;
            text-align: center;
            cursor: pointer;
            color: #666;
            font-weight: 600;
        }
        #result li.more-btn:hover { background: #ddd; }
        #restart {
            display: none;
            margin: 20px auto;
            padding: 12px 32px;
            font-size: 1rem;
            border: none;
            border-radius: 8px;
            background: #333;
            color: #fff;
            cursor: pointer;
        }
        #restart:hover { background: #555; }
    </style>
</head>
<body>
    <h1>나의 취미 찾기</h1>
    <p id="question" style="text-align:center; margin-bottom:16px; font-size:1.2rem; color:#555;"></p>
    <div class="grid" id="grid"></div>
    <div id="result">
        <h2 id="result-title"></h2>
        <ul id="result-list"></ul>
    </div>
    <button id="restart" onclick="reset()">처음부터 다시하기</button>

    <script>
        const labels = { "1": "만들기", "2": "소비하기", "3": "움직이기", "4": "커뮤니티" };
        const colors = { "1": "#4CAF50", "2": "#2196F3", "3": "#FF9800", "4": "#9C27B0" };
        let step = 1;
        let primary = null;

        function render() {
            const grid = document.getElementById("grid");
            const question = document.getElementById("question");
            grid.innerHTML = "";

            if (step === 1) {
                question.textContent = "가장 필요한 옵션은 무엇인가요?";
            } else {
                question.textContent = "추가로 원하는 옵션이 있나요?";
            }

            const ids = ["1", "2", "3", "4"];

            ids.forEach(id => {
                const cell = document.createElement("div");
                cell.className = "cell";
                cell.dataset.id = id;
                cell.style.background = colors[id];

                if (step === 2 && id === primary) {
                    cell.classList.add("proceed");
                    cell.textContent = labels[id] + "만으로 진행";
                    cell.onclick = () => showResult(primary);
                } else if (step === 2) {
                    cell.textContent = labels[id];
                    cell.onclick = () => {
                        const key = primary < id ? primary + id : id + primary;
                        showResult(key);
                    };
                } else {
                    cell.textContent = labels[id];
                    cell.onclick = () => selectPrimary(id);
                }

                grid.appendChild(cell);
            });
        }

        function selectPrimary(id) {
            primary = id;
            step = 2;
            render();
        }

        let currentKey = null;

        async function showResult(key) {
            currentKey = key;
            const res = await fetch("/api/hobbies/" + key);
            const data = await res.json();

            document.getElementById("grid").style.display = "none";
            document.getElementById("question").style.display = "none";
            const result = document.getElementById("result");
            result.style.display = "block";
            document.getElementById("result-title").textContent = data.label + " 추천 취미";
            const list = document.getElementById("result-list");
            list.innerHTML = "";
            data.hobbies.forEach(h => {
                const li = document.createElement("li");
                if (h === "다른 취미 더보기") {
                    li.textContent = h;
                    li.classList.add("more-btn");
                    li.onclick = () => loadExtra(key);
                } else {
                    li.textContent = h;
                }
                list.appendChild(li);
            });
            document.getElementById("restart").style.display = "block";
        }

        async function loadExtra(key) {
            const res = await fetch("/api/hobbies/" + key + "/extra");
            const data = await res.json();
            const list = document.getElementById("result-list");
            const moreBtn = list.querySelector(".more-btn");
            if (moreBtn) moreBtn.remove();
            data.extra_hobbies.forEach(h => {
                const li = document.createElement("li");
                li.textContent = h;
                list.appendChild(li);
            });
        }

        function reset() {
            step = 1;
            primary = null;
            document.getElementById("grid").style.display = "grid";
            document.getElementById("question").style.display = "block";
            document.getElementById("result").style.display = "none";
            document.getElementById("restart").style.display = "none";
            render();
        }

        render();
    </script>
</body>
</html>
"""
