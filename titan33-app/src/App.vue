<template>
  <div class="tradingview-style-app">
    <div class="tv-header">
      <div class="tv-logo">
        <!-- SVG Logo -->
        <svg width="50" height="50" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
          <circle cx="50" cy="50" r="48" stroke="#4a90e2" stroke-width="4" fill="none" />
          <text x="50%" y="50%" text-anchor="middle" fill="#4a90e2" font-size="24" font-family="Roboto" dy=".3em">W33B</text>
        </svg>
      </div>
      <h1>基于大模型的股票投资系统</h1>
    </div>
    <div class="tv-container">
      <div class="tv-sidebar">
        <!-- 股票选择 -->
        <div class="tv-sidebar-section">
          <h2>选择股票</h2>
          <input type="text" v-model="searchQuery" placeholder="搜索股票..." class="tv-search-input" />
          <select v-model="selectedStocks" multiple class="tv-multi-select">
            <option v-for="stock in filteredStocks" :key="stock.symbol" :value="stock.symbol">
              {{ stock.name }} ({{ stock.symbol }})
            </option>
          </select>
        </div>
        <!-- 算法选择 -->
        <div class="tv-sidebar-section">
          <h2>选择算法</h2>
          <select v-model="selectedAlgorithm" class="tv-select">
            <option value="A2C">A2C (Advantage Actor-Critic)</option>
            <option value="DDPG">DDPG (Deep Deterministic Policy Gradient)</option>
          </select>
        </div>
        <!-- 时间选择 -->
        <div class="tv-sidebar-section">
          <h2>选择训练时间范围</h2>
          <div class="tv-date-range">
            <input type="date" v-model="selectedStartTime" class="tv-date-picker" />
            <span>至</span>
            <input type="date" v-model="selectedEndTime" class="tv-date-picker" />
          </div>
        </div>
        <div class="tv-sidebar-section">
          <h2>选择预测时间范围</h2>
          <div class="tv-date-range">
            <input type="date" v-model="selectedStartTradeTime" class="tv-date-picker" />
            <span>至</span>
            <input type="date" v-model="selectedEndTradeTime" class="tv-date-picker" />
          </div>
        </div>
      </div>
      <div class="tv-main-content">
        <!-- 配置摘要 -->
        <div class="tv-summary">
          <h2>已选择的配置清单</h2>
          <ul v-if="selectedStocks.length > 0">
            <li v-for="stockSymbol in selectedStocks" :key="stockSymbol">
              {{ getStockNameBySymbol(stockSymbol) }} ({{ stockSymbol }})
            </li>
          </ul>
          <div v-if="selectedAlgorithm">
            算法: {{ selectedAlgorithm }}
          </div>
          <div v-if="selectedStartTime && selectedEndTime">
            训练时间范围: {{ selectedStartTime }} 至 {{ selectedEndTime }}
          </div>
          <div v-if="selectedStartTradeTime && selectedEndTradeTime">
            预测时间范围: {{ selectedStartTradeTime }} 至 {{ selectedEndTradeTime }}
          </div>
        </div>
        <!-- 按钮组 -->
        <div class="tv-button-group">
          <button @click="startTraining" class="tv-btn">启动训练</button>
          <button @click="showCapitalCurve" class="tv-btn">查看回测资金曲线</button>
          <button @click="showTrainingResults" class="tv-btn">查看回测结果</button>
        </div>
        <div v-if="showTrainingResultsModal" class="training-results-modal">
          <h2>回测结果</h2>
          <table>
            <thead>
              <tr>
                <th>指标</th>
                <th v-for="agent in Object.keys(performanceData)" :key="agent">{{ agent }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(metric, index) in Object.keys(performanceData[Object.keys(performanceData)[0]])" :key="index">
                <th>{{ metric }}</th>
                <td v-for="(agent, i) in Object.keys(performanceData)" :key="i">{{ formatValue(performanceData[agent][metric]) }}</td>
              </tr>
            </tbody>
          </table>
          <button @click="hideTrainingResults" class="tv-btn">关闭</button>
        </div>
      </div>
    </div>
    <div v-if="showCapitalCurveModal" class="capital-curve-modal">
      <img :src="capitalCurveImageUrl" alt="Capital Curve" />
      <button @click="hideCapitalCurve" class="tv-btn">关闭</button>
    </div>
    <!-- 自定义警告模态框 -->
    <div v-if="showAlert" class="custom-alert-modal">
      <div class="custom-alert-content">
        <h2>警告</h2>
        <p>{{ alertMessage }}</p>
        <button @click="closeAlert" class="tv-btn">关闭</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';

import axios from 'axios';
// 假设 stocks 是一个包含股票信息的数组，你需要根据实际情况提供这个数据

const stocks = ref([
  { name: '浦发银行', symbol: '600000.SH' },
  { name: '上海机场', symbol: '600009.SH' },
  { name: '民生银行', symbol: '600016.SH' },
  { name: '中国石化', symbol: '600028.SH' },
  { name: '中信证券', symbol: '600030.SH' },
  { name: '三一重工', symbol: '600031.SH' },
  { name: '招商银行', symbol: '600036.SH' },
  { name: '中国联通', symbol: '600050.SH' },
  { name: '恒生电子', symbol: '600570.SH' },
  { name: '山东黄金', symbol: '600547.SH' },

]);

export default {
  setup() {
    // 选中的股票符号
    const selectedStocks = ref([]);
    // 选择的算法
    const selectedAlgorithm = ref('A2C');
    // 选择的开始时间
    const selectedStartTime = ref('');
    // 选择的结束时间
    const selectedEndTime = ref('');

    // 选择的开始时间
    const selectedStartTradeTime = ref('');
    // 选择的结束时间
    const selectedEndTradeTime = ref('');
    const performanceData = ref({
  DDPG: {
    Annual_return: 0.0000,
    Cumulative_returns: 0.00000,
    Annual_volatility: NaN,
    Sharpe_ratio: NaN,
    Stability: 0.0,
    Max_drawdown: 0.0,
    Kurtosis: NaN,
    Tail_ratio: 0.0,
    Daily_value_at_risk: NaN
  },
  A2C: {
    Annual_return: 0.0000,
    Cumulative_returns: 0.00000,
    Annual_volatility: NaN,
    Sharpe_ratio: NaN,
    Stability: 0.0,
    Max_drawdown: 0.0,
    Kurtosis: NaN,
    Tail_ratio: 0.0,
    Daily_value_at_risk: NaN
  }
});
    // 获取股票名称的方法
    const getStockNameBySymbol = (symbol) => {
      const stock = stocks.value.find(s => s.symbol === symbol);
      return stock ? stock.name : '未知股票';
    };

    // 启动训练的方法
    const startTraining = async () => {
      if (selectedStocks.value.length > 0 && selectedAlgorithm.value && selectedStartTime.value && selectedEndTime.value) {
        // 这里可以调用后端 API 启动训练，或者执行其他逻辑
       
        try {
          alert('训练已开始，请稍后查看训练结果');
          const response = await axios.post('http://127.0.0.1:5000/start-train', {
            stocks: selectedStocks.value,
            algorithm: selectedAlgorithm.value,
            start_time: selectedStartTime.value,
            end_time: selectedEndTime.value,
            tradestart: selectedStartTradeTime.value,
            tradeend: selectedEndTradeTime.value
          });
          // 处理后端返回的响应
          if (response.status === 200) {
            // 可以在这里显示一个消息或导航到另一个页面
            alert('训练已结束，请查看训练结果:' + response.data);
            performanceData.value = response.data
            console.log(response.data);
          } else {
            alert('后端返回错误，状态码：' + response.status);
          }
        } catch (error) {
          console.error('启动训练失败:', error);
          alert('启动训练失败，请检查后端服务。');
        }
      } else {
        alert('请完成所有配置选项后再启动训练！');
      }
    };
    const showCapitalCurveModal = ref(false);
    const showTrainingResultsModal = ref(false);

    const capitalCurveImageUrl = ref('');

    const showCapitalCurve = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/get-capital-curve',{
    responseType: 'blob'
});
        capitalCurveImageUrl.value = URL.createObjectURL(response.data);
        showCapitalCurveModal.value = true;
      } catch (error) {
        console.error('Error fetching capital curve:', error);
      }
    };

    const hideCapitalCurve = () => {
      showCapitalCurveModal.value = false;
      URL.revokeObjectURL(capitalCurveImageUrl.value);
    };


    const showTrainingResults = () => {
      showTrainingResultsModal.value = true;
    };

    const hideTrainingResults = () => {
      showTrainingResultsModal.value = false;
    };

    const formatValue = (value) => {

        return value; // 其他类型的值，直接返回
      
    };

    return {
      stocks,
      selectedStocks,
      selectedAlgorithm,
      selectedStartTime,
      selectedEndTime,
      getStockNameBySymbol,
      startTraining,
      showCapitalCurve,
      hideCapitalCurve,
      showTrainingResults,
      hideTrainingResults,
      showCapitalCurveModal,
      showTrainingResultsModal,
      capitalCurveImageUrl,
      selectedStartTradeTime,
      selectedEndTradeTime,
      performanceData,
      formatValue
    };
  }
};
</script>
<style scoped>
.tradingview-style-app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #1e1e2f;
  font-family: 'Roboto', sans-serif;
  color: #e0e0e0;
  padding: 20px;
}

.tv-header {
  display: flex;
  align-items: center;
  padding: 20px;
  background-color: #28293e;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  margin-bottom: 20px;
}

.tv-logo {
  margin-right: 20px;
}

.tv-container {
  display: flex;
  flex-grow: 1;
  gap: 20px;
}

.tv-sidebar {
  flex: 0 0 250px;
  background-color: #28293e;
  padding: 20px;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.tv-main-content {
  flex-grow: 1;
  background-color: #1e1e2f;
  overflow-x: auto;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.tv-sidebar-section {
  margin-bottom: 30px;
}

.tv-sidebar-section h2 {
  margin-bottom: 20px;
  color: #4a90e2;
}

.tv-search-input {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  border-radius: 4px;
  border: 1px solid #555;
  background-color: #333;
  color: #e0e0e0;
}

.tv-multi-select {
  width: 100%;
  height: 150px;
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #555;
  background-color: #333;
  color: #e0e0e0;
  overflow-y: auto;
}

.tv-select, .tv-date-picker {
  padding: 8px 10px;
  background-color: #333;
  color: #e0e0e0;
  border: 1px solid #555;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.3s, box-shadow 0.3s;
  width: 100%;
  margin-bottom: 10px;
}

.tv-date-range {
  display: flex;
  align-items: center;
  gap: 10px;
}

.tv-btn {
  padding: 10px 20px;
  background-color: #4a90e2;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
  width: 100%;
  margin-bottom: 10px;
}

.tv-btn:hover {
  background-color: #3d7ec1;
  transform: translateY(-2px);
}

.tv-button-group {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.capital-curve-modal, .training-results-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.9); /* 更深的背景以突出内容 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10;
  opacity: 0;
  animation: fadeIn 0.3s forwards;
}

.training-results-modal {
  background-color: #2a2a3b;
  padding: 40px; /* 增加内边距 */
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  width: 90%; /* 几乎占满整个屏幕宽度 */
  height: 90%; /* 几乎占满整个屏幕高度 */
  overflow-y: auto;
}

.training-results-modal button {
  padding: 10px 20px;
  background-color: #4a90e2;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
  position: absolute;
  top: 20px;
  right: 20px;
}

.training-results-modal button:hover {
  background-color: #3d7ec1;
  transform: translateY(-2px);
}

.performance-comparison {
  margin: 20px;
  font-family: 'Roboto', sans-serif;
}

table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
  margin-top: 20px;
}

th, td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #444;
}

thead th {
  background-color: #4a90e2;
  color: #fff;
}

td {
  font-weight: lighter;
}

td:nth-child(even) {
  background-color: #2a2a3b;
}

th, td {
  transition: background-color 0.3s;
}

th:hover, td:hover {
  background-color: #3d3d4f;
}

th {
  text-transform: uppercase;
  font-size: 0.8em;
  letter-spacing: 0.5px;
  padding: 10px 5px;
}

td {
  font-size: 0.9em;
  padding: 15px 5px;
}

@keyframes fadeIn {
  to {
    opacity: 1;
  }
}

.custom-alert-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 20;
  animation: fadeIn 0.3s forwards;
}

.custom-alert-content {
  background-color: #2a2a3b;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  text-align: center;
  max-width: 400px;
  width: 90%;
}

.custom-alert-content h2 {
  color: #e0e0e0;
  margin-bottom: 20px;
}

.custom-alert-content p {
  color: #e0e0e0;
  margin-bottom: 20px;
}
</style>