import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import { ConfigProvider } from "antd";
import ruRU from "antd/locale/ru_RU";
import dayjs from "dayjs";
import "dayjs/locale/ru";

import App from "./App";
import "./index.css";

// Локализация dayjs — русский язык, неделя начинается с понедельника
dayjs.locale("ru");

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ConfigProvider
      locale={ruRU}
      theme={{
        token: {
          colorPrimary: "#13c2c2", // бирюзовый — основной цвет приложения
        },
      }}
    >
      <App />
    </ConfigProvider>
  </StrictMode>
);
