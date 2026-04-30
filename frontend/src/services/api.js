import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "/",
});

export const uploadDocument = async (file) => {
  const formData = new FormData();
  formData.append("file", file);
  const { data } = await api.post("/api/documents/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
};

export const getDocuments = async () => {
  const { data } = await api.get("/api/documents");
  return data;
};

export const getDocument = async (documentId) => {
  const { data } = await api.get(`/api/documents/${documentId}`);
  return data;
};

export const processDocument = async (documentId) => {
  const { data } = await api.post(`/api/process/${documentId}`);
  return data;
};

export const searchDocuments = async (query, topK = 5) => {
  const { data } = await api.post("/api/search", { query, top_k: topK });
  return data;
};

export const askQuestion = async (question, topK = 4) => {
  const { data } = await api.post("/api/ask", { question, top_k: topK });
  return data;
};

export const getDashboardMetrics = async () => {
  const { data } = await api.get("/api/dashboard/metrics");
  return data;
};

export default api;
