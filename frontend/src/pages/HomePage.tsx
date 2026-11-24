/**
 * Главная страница — проверка связи с backend.
 */
import { Typography, Card, Tag, Spin } from "antd";
import { AppLayout } from "@/components/AppLayout";
import { useHealthCheck } from "@/hooks/useHealthCheck";

const { Title, Paragraph } = Typography;

export function HomePage() {
  const { data, isLoading, isError } = useHealthCheck();

  return (
    <AppLayout>
      <Card>
        <Title level={2}>Cat Health Tracker</Title>
        <Paragraph>Мониторинг здоровья кошек</Paragraph>

        <Paragraph>
          API статус:{" "}
          {isLoading && <Spin size="small" />}
          {isError && <Tag color="red">недоступен</Tag>}
          {data && (
            <Tag color={data.status === "ok" ? "green" : "red"}>
              {data.status === "ok" ? "работает" : data.status}
            </Tag>
          )}
          {data && (
            <span style={{ color: "#999", marginLeft: 8 }}>
              v{data.version}
            </span>
          )}
        </Paragraph>

        <Paragraph type="secondary">
          Приложение настроено. Функциональность будет добавлена на следующих
          этапах разработки.
        </Paragraph>
      </Card>
    </AppLayout>
  );
}
