import { api } from "./api";

export const getServices = () => api.get("/services");
export const createService = (data: { name: string; status: string }) =>
  api.post("/services", data);
