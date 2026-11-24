/**
 * Страница 404.
 */
import { Typography } from "antd";
import { AppLayout } from "@/components/AppLayout";

const { Title, Paragraph } = Typography;

export function NotFoundPage() {
  return (
    <AppLayout>
      <Title level={2}>404</Title>
      <Paragraph>Страница не найдена.</Paragraph>
    </AppLayout>
  );
}
