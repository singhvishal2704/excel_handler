import React, { useState } from "react";
import { useAppDispatch, useAppSelector } from "../hooks/useTypedRedux";
import { setData, setLoading, setError } from "../store/slices/excelSlice";
import { postOperation, getProcessedData } from "../services/api";
import Modal from "./Modal";
import toast from "react-hot-toast";

const OperationsPanel: React.FC = () => {
  const dispatch = useAppDispatch();
  const sessionId = useAppSelector((state) => state.excel.sessionId);
  const data = useAppSelector((state) => state.excel.data);

  const [modalType, setModalType] = useState<"add_column" | "filter" | null>(
    null,
  );
  const [expression, setExpression] = useState("");
  const [newColumn, setNewColumn] = useState("");
  const [filterColumn, setFilterColumn] = useState("");
  const [filterOperator, setFilterOperator] = useState(">");
  const [filterValue, setFilterValue] = useState("");
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const fetchData = async () => {
    if (!sessionId) return;
    dispatch(setLoading(true));
    try {
      const rows = await getProcessedData(sessionId);
      dispatch(setData(rows));
    } catch (err: any) {
      dispatch(setError("Fetching data failed"));
      setErrorMsg(err.message || "Something went wrong");
    } finally {
      dispatch(setLoading(false));
    }
  };

  const closeModal = () => {
    setModalType(null);
    setExpression("");
    setNewColumn("");
    setFilterColumn("");
    setFilterOperator(">");
    setFilterValue("");
    setErrorMsg(null);
  };

  const handleSubmit = async () => {
    if (!sessionId) return;
    dispatch(setLoading(true));
    try {
      let payload: any = {};

      if (modalType === "add_column") {
        payload = {
          operation: "add_column",
          new_column: newColumn,
          expression: `${newColumn} = ${expression}`,
        };
      } else if (modalType === "filter") {
        payload = {
            operation: "filter_rows",
            expression,
        };
      }

      const response = await postOperation(sessionId, payload);

      if (Array.isArray(response) && response.length > 0) {
        dispatch(setData(response));
        toast.success("Operation successful.");
      } else {
        toast.error("Operation failed.");
      }
    } catch (err: any) {
      dispatch(setError("Operation failed"));
      setErrorMsg(err.response.data.message || "Something went wrong");
      toast.error(err.response.data.message || "Something went wrong");
    } finally {
      dispatch(setLoading(false));
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap gap-4">
        <button
          onClick={() => setModalType("add_column")}
          className="rounded bg-blue-600 px-4 py-2 text-white"
        >
          Add Column
        </button>
        <button
          onClick={() => setModalType("filter")}
          className="rounded bg-green-600 px-4 py-2 text-white"
        >
          Filter Rows
        </button>
        <button
          onClick={fetchData}
          className="rounded bg-gray-600 px-4 py-2 text-white"
        >
          Refresh Table
        </button>
      </div>

      {data.length > 0 && (
        <div className="overflow-x-auto rounded border">
          <table className="min-w-full text-left text-sm">
            <thead className="bg-gray-100">
              <tr>
                {Object.keys(data[0]).map((key) => (
                  <th key={key} className="border-b px-4 py-2 font-semibold">
                    {key}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.map((row, idx) => (
                <tr key={idx} className="hover:bg-gray-50">
                  {Object.values(row).map((value, i) => (
                    <td key={i} className="border-b px-4 py-2">
                      {String(value)}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <Modal
        isOpen={modalType === "add_column"}
        onClose={closeModal}
        title="Add Column"
      >
        <input
          type="text"
          placeholder="New column name"
          className="mb-3 w-full rounded border p-2"
          value={newColumn}
          onChange={(e) => setNewColumn(e.target.value)}
        />
        <input
          type="text"
          placeholder="Expression (e.g. Sales Price + Tax)"
          className="mb-3 w-full rounded border p-2"
          value={expression}
          onChange={(e) => setExpression(e.target.value)}
        />
        {errorMsg && <p className="mb-2 text-sm text-red-500">{errorMsg}</p>}
        <button
          onClick={handleSubmit}
          className="mt-2 w-full rounded bg-primary px-4 py-2 text-white"
        >
          Apply
        </button>
      </Modal>

      <Modal
        isOpen={modalType === "filter"}
        onClose={closeModal}
        title="Filter Rows"
      >
        <input
          type="text"
          placeholder="Expression (e.g. Filter rows where Sales Price is greater than 500)"
          className="mb-3 w-full rounded border p-2"
          value={expression}
          onChange={(e) => setExpression(e.target.value)}
        />
        {errorMsg && <p className="mb-2 text-sm text-red-500">{errorMsg}</p>}
        <button
          onClick={handleSubmit}
          className="mt-2 w-full rounded bg-primary px-4 py-2 text-white"
        >
          Apply
        </button>
      </Modal>
    </div>
  );
};

export default OperationsPanel;
