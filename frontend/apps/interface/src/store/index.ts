import Vuex from 'vuex'
import Vue from 'vue'
import auth from './auth'
// import example from './module-example';
// import { ExampleStateInterface } from './module-example/state';

/*
 * If not building with SSR mode, you can
 * directly export the Store instantiation
 */

export interface StateInterface {
  // Define your own store structure, using submodules if needed
  // example: ExampleStateInterface;
  // Declared as unknown to avoid linting issue. Best to strongly type as per the line above.
  example: unknown;
}

Vue.use(Vuex)

const Store = new Vuex.Store<StateInterface>({
  modules: {
    auth
  },
  strict: !!process.env.DEBUGGING
})

export default Store
