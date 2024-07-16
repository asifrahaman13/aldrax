import { CheckCircleIcon } from '@heroicons/react/20/solid';

export default function SuccessAlert() {
  return (
    <div className="rounded-md bg-green-50 z-50 fixed w-screen p-4">
      <div className="flex">
        <div className="flex-shrink-0">
          <CheckCircleIcon
            aria-hidden="true"
            className="h-5 w-5 text-green-400"
          />
        </div>
        <div className="ml-3">
          <h3 className="text-sm font-medium text-green-800">
            Order completed
          </h3>
          <div className="mt-2 text-sm text-green-700">
            <p>Data added successfully</p>
          </div>
        </div>
      </div>
    </div>
  );
}
