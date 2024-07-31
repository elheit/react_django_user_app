import { create } from "zustand";
import { mountStoreDevtool } from "simple-zustand-devtools";

const useAuthStore = create((set, get) => ({
  allUserData: null,
  loading: false,

  user: () => ({
    user_id: get().allUserData?.user_id || null,
    username: get().allUserData?.username || null,
  }),

  setUser: (user) =>
    set({
      allUserData: user,
    }),
  setLOading: (loading) => set({ loading }),
  isLoggedIn: () => get().allUserData !== null,
}));

if (import.meta.env.DEV) {
  mountStoreDevtool("StoreAuth", useAuthStore);
}

export { useAuthStore };
