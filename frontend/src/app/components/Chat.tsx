'use client';
import React, { useEffect, useRef, useState } from 'react';
import { conversationStaticTexts } from '@/constants/static/staticTexts/staticTexts';
import { Status } from '@/constants/types/type.query';
import RenderConversation from '@/app/components/RenderConversation';
import { useDispatch } from 'react-redux';
import { setHistory } from '@/lib/conversation/conversationSlice';

export default function Chat() {
  const db = 'sqlite';
  const websocketRef = useRef<WebSocket | null>(null);
  const [status, setStatus] = useState<Status>({
    message: '',
    status: false,
  });

  const dispatch = useDispatch();

  useEffect(() => {
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_SOCKET || '';
    const accessToken = localStorage.getItem('accessToken');
    const websocket = new WebSocket(
      `${backendUrl}/query/sqlite-query/${accessToken}`
    );
    websocketRef.current = websocket;
    websocket.onopen = () => {
      console.log('Connected to websocket');
    };

    websocket.onmessage = (event) => {
      const parsedData = JSON.parse(event.data);
      console.log('############ The parsed data is :', parsedData);
      if (parsedData.status === true) {
        setStatus({
          message: parsedData.message,
          status: true,
        });
        return;
      }
      if (parsedData.answer_type === 'sql_query') {
        console.log('############ Triggered The parsed data is :', parsedData);
        setStatus({
          message: parsedData.sql_query,
          status: false,
        });
      } else {
        setStatus({
          message: 'Error in the query',
          status: false,
        });
      }

      console.log('##########################', status);
      dispatch(
        setHistory({
          message: parsedData?.message,
          sql_query: parsedData?.sql_query,
          messageFrom: 'chatbot',
          answer_type: parsedData?.answer_type,
        })
      );
    };

    websocket.onclose = () => {
      console.log('Disconnected from websocket');
    };

    return () => {
      websocket.close();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <React.Fragment>
      <div className="w-full items-center py-4 justify-center h-screen overflow-y-hidden flex flex-col bg-gray-50">
        <RenderConversation
          websocketRef={websocketRef}
          texts={conversationStaticTexts}
          status={status}
          db={db}
        />
      </div>
    </React.Fragment>
  );
}
