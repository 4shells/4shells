// Third party libraries
import { useEffect, useState } from 'react';

export const DATA_URL = 'https://raw.githubusercontent.com/kamadorueda/four-shells/data-nixdb';

const fetchJSON = async (url) => {
  let response = await fetch(url);

  while (!response.ok || response.status !== 200) {
    response = await fetch(url);
  }

  return await response.json();
};

export const useFetchJSON = (url, defaultData) => {
  const [data, setData] = useState(defaultData);

  useEffect(() => {
    (async () => setData(await fetchJSON(`${DATA_URL}${url}`)))();
  }, [url]);

  return data;
}
