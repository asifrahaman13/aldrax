import { ExclamationTriangleIcon } from '@heroicons/react/20/solid';

export default function ErrorAlert() {
  return (
    <div className="border-l-4 fixed border-yellow-400 top-2 bg-yellow-50 p-4">
      <div className="flex">
        <div className="flex-shrink-0">
          <ExclamationTriangleIcon
            aria-hidden="true"
            className="h-5 w-5 text-yellow-400"
          />
        </div>
        <div className="ml-3">
          <p className="text-sm text-yellow-700">
            You cannot have blank messages{' '}
          </p>
        </div>
      </div>
    </div>
  );
}
