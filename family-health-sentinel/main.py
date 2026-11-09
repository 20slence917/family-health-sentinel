"""家庭健康哨兵 - Web 服务入口

DevCloud 部署要求：
- 监听端口 8080（平台仅路由此端口）
- 绑定 0.0.0.0（localhost 在容器外不可见）
- 生产环境关闭 debug 模式
"""

from flask import Flask, jsonify

app = Flask(__name__)

# 简易健康知识库（示例数据）
HEALTH_TIPS = {
    "hypertension": {
        "name": "高血压",
        "diet": "低盐少油，每日盐不超过5g；忌腌制品、浓肉汤；宜芹菜、木耳、低脂牛奶",
    },
    "diabetes": {
        "name": "糖尿病",
        "diet": "主食粗细搭配，先菜后肉再饭；忌甜食、白粥；宜杂粮、绿叶菜、低糖水果",
    },
    "gout": {
        "name": "痛风",
        "diet": "忌海鲜、浓肉汤、动物内脏、啤酒；宜低脂牛奶、鸡蛋、多喝水（每天2000ml+）",
    },
}


@app.route("/")
def index():
    """首页：服务介绍"""
    return jsonify({
        "service": "家庭健康哨兵",
        "status": "running",
        "endpoints": {
            "健康检查": "/health",
            "饮食建议": "/diet/<condition>",
            "支持病种": "/conditions",
        },
        "disclaimer": "本服务仅供健康参考，不能替代执业医师的当面诊断",
    })


@app.route("/health")
def health():
    """健康检查端点（DevCloud 容器探活）"""
    return jsonify({"status": "ok"})


@app.route("/conditions")
def conditions():
    """返回支持的病种列表"""
    return jsonify({key: value["name"] for key, value in HEALTH_TIPS.items()})


@app.route("/diet/<condition>")
def diet(condition):
    """按病种返回饮食建议"""
    if condition not in HEALTH_TIPS:
        return jsonify({"error": f"暂不支持该病种: {condition}",
                        "supported": list(HEALTH_TIPS.keys())}), 404
    info = HEALTH_TIPS[condition]
    return jsonify({
        "condition": info["name"],
        "diet_advice": info["diet"],
        "disclaimer": "仅供参考，具体饮食方案请遵医嘱",
    })


if __name__ == "__main__":
    # DevCloud 规则：端口 8080，绑定 0.0.0.0，关闭 debug
    app.run(host="0.0.0.0", port=8080, debug=False)