/**
 * Хук для проверки состояния API.
 */
import { useQuery } from "@tanstack/react-query";
import { apiClient } from "@/api/client";
import type { HealthResponse } from "@/types";

export function useHealthCheck() {
  return useQuery<HealthResponse>({
    queryKey: ["health"],
    queryFn: async () => {
      const { data } = await apiClient.get<HealthResponse>("/health");
      return data;
    },
    staleTime: 30000,
  });
}
