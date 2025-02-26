import handleDelete from "../../list/TableTemplate/DeleteHandler";

export const handleDeleteAction = (props) => {
  const { endpoint, openModal, setLoading, navigateUp: refresh, id } = props;
  handleDelete({
    id,
    endpoint,
    openModal,
    setLoading,
    refresh,
  });
};
