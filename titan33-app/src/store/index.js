import { createStore } from 'vuex';

export default createStore({
  state: {
    selectedStock: null,
  },
  mutations: {
    setSelectedStock(state, stock) {
      state.selectedStock = stock;
    },
  },
});