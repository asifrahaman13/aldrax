import { SiSqlite } from 'react-icons/si';
const TITLE = {
  sqlite: 'SQLite',
} as const;

const ICONS = {
  sqlite: SiSqlite,
} as const;

export interface Status {
  message: string;
  status: boolean;
}

export interface HistoryItem {
  message: string;
  messageFrom: string;
  answer_type?: string;
}

export interface RenderConversationProps {
  websocketRef: React.MutableRefObject<WebSocket | null>;
  texts: string[];
  status: Status;
  db: IconKey;
}

export interface IconComponentsProps {
  props: {
    slug: TitleKeys;
  };
}

export { TITLE, ICONS };
export type IconKey = keyof typeof ICONS;
export type TitleKeys = keyof typeof TITLE;
