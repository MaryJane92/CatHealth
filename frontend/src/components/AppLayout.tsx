/**
 * Базовый layout приложения.
 * Заголовок и навигация будут добавлены на следующих этапах.
 */
import { Layout, Typography } from "antd";

const { Header, Content } = Layout;
const { Title } = Typography;

export function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Header style={{ display: "flex", alignItems: "center" }}>
        <Title level={4} style={{ color: "white", margin: 0 }}>
          🐱 Cat Health Tracker
        </Title>
      </Header>
      <Content style={{ padding: "24px" }}>
        <div style={{ maxWidth: 1200, margin: "0 auto" }}>{children}</div>
      </Content>
    </Layout>
  );
}
