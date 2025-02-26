import React, { useState, useEffect, useRef } from "react"; // Import useRef
import DocHeader from "@/components/core/common/header/DocHeader";
import { useConfig } from "@/contexts/ConfigContext";
import useKeyEvents from "@/hooks/useKeyEvents";
import { useRouter } from "next/router";
import DetailForm from "./DetailForm";
import { useData } from "@/contexts/DataContext";
import { toUnderscoreLowercase } from "@/utils/textConvert";
import * as buttonActions from "./actions";
import { defaultButtons } from "./buttonConfig";
import { useModal } from "@/contexts/ModalContext";
import ToastTemplates from "@/components/core/common/toast/ToastTemplates";
import _ from "lodash";
import SendEmail from "@/components/functions/communication/SendEmail";
import SendSms from "@/components/functions/communication/SendSms";
import { findDocDetails } from "@/utils/findDocDetails";
import { importFile } from "@/utils/importFile";

const DoctypeForm = ({
  handleSave,
  config,
  additionalButtons = [],
  is_doc = true,
}) => {
  const { localConfig, localAppData, setLocalConfig, setLocalAppData  } = useConfig();
  const { form, setForm, setLoading, data, setData } = useData();
  const [isEditing, setIsEditing] = useState(false);
  const [smsModalOpen, setSmsModalOpen] = useState(false);
  const [emailModalOpen, setEmailModalOpen] = useState(false);
  const router = useRouter();
  const { openModal } = useModal();
  const endpoint = localAppData?.endpoint;
  const { slug, id } = router.query;

  const formRef = useRef(null); // Create a reference for the form

  useEffect(() => {
    setIsEditing(true);
  }, [localConfig]);

   useEffect(() => {
        
        if (!slug) return;
    
        const fetchDocumentData = async () => {
          try {
            // Fetch document details
            const docData = findDocDetails(slug);
            if (!docData) throw new Error("Failed to fetch document details");
    
            setLocalAppData({ ...docData, endpoint: `${docData.app_id}/${slug}` });
    
            // Fetch configuration data
            const configData = await importFile(slug, `${slug}.json`);
            if (!configData) throw new Error("Failed to load configuration");
    
            setLocalConfig(configData.content);
  
          } catch (error) {
            console.error(error.message);
          }
        };
    
        fetchDocumentData();
      }, [slug]);

  const handleSaveClick = (event) => {
    event.preventDefault(); // Prevent default form submission

    // Validate required fields
    const missingFields = [];
    localConfig?.field_order.forEach((fieldName) => {
      const field = Object.values(localConfig?.fields || {}).find(
        (f) => f.fieldname === fieldName
      );

      if (
        field?.reqd &&
        (!form[fieldName] || form[fieldName].toString().trim() === "")
      ) {
        missingFields.push(field.label || fieldName); // Use label if available, otherwise field name
      }
    });

    if (missingFields.length > 0) {
      ToastTemplates.warning(
        `Please fill in the required fields: ${missingFields.join(", ")}`
      );
      return; // Stop form submission
    }

    // Function to clean form data
    const cleanData = (data) => {
      if (data instanceof Date) return data;

      if (Array.isArray(data)) {
        return data
          .map(cleanData)
          .filter(
            (item) =>
              item !== null &&
              item !== undefined &&
              item !== "" &&
              (typeof item !== "object" || Object.keys(item).length > 0)
          );
      }

      if (typeof data === "object" && data !== null) {
        return Object.fromEntries(
          Object.entries(data)
            .map(([key, value]) => [key, cleanData(value)])
            .filter(
              ([_, value]) =>
                value !== null &&
                value !== undefined &&
                value !== "" &&
                (typeof value !== "object" || Object.keys(value).length > 0)
            )
        );
      }

      return data;
    };

    const cleanedForm = cleanData(form);
    handleSave(cleanedForm);
  };

  useKeyEvents(
    () => {},
    handleSaveClick,
    (props) => buttonActions.handleDuplicate(props)
  );

  const wrapButtonProperties = (button, additionalProps) => {
    const wrappedButton = {
      ...button,
      ...additionalProps,
    };
    if (button.action) {
      wrappedButton.action = (event) => {
        button.action({ ...additionalProps, event });
      };
    }
    return wrappedButton;
  };

  const navigateUp = () => {
    const currentPath = router.asPath;
    const segments = currentPath.split("/").filter(Boolean);
    if (segments.length > 1) {
      segments.pop();
    }
    const newPath = `/${segments.join("/")}`;
    router.push(newPath);
  };

  const reloadData = () => {
    router.reload();
  };

  const sharedProps = {
    router,
    id,
    form,
    setForm,
    localConfig,
    openModal,
    endpoint,
    setLoading,
    navigateUp,
    data,
    setData,
    reloadData,
    slug,
    setSmsModalOpen,
    setEmailModalOpen,
  };

  const buttons = [...defaultButtons, ...additionalButtons].map((button) =>
    wrapButtonProperties(button, sharedProps)
  );

  const link = is_doc
    ? `/app/${toUnderscoreLowercase(localConfig?.name)}`
    : `/${toUnderscoreLowercase(localConfig?.name)}`;

  useEffect(() => {
    if (!_.isEqual(form, data)) {
      setIsEditing(true);
    } else {
      setIsEditing(false);
    }
  }, [form, data]);
  return (
    <div className="flex flex-col">
      <DocHeader
        isEditing={isEditing}
        handleEditClick={() =>
          buttonActions.handleEditClick(setIsEditing, { id, config, router })
        }
        handleSaveClick={handleSaveClick}
        title={localConfig?.name}
        buttons={buttons}
        link={link}
      />
      <div
        // ref={formRef}
        // onSubmit={handleFormSubmit}
        className="relative z-1 px-4 flex flex-col mt-2 w-full"
      >
        <div className="h-full shadow-md shadow-slate-300">
          <DetailForm />
        </div>
      </div>
      <SendEmail
        isOpen={emailModalOpen}
        msg={"Hi, "}
        email={form?.email || form?.user?.email || form?.customer?.email}
        onRequestClose={() => setEmailModalOpen(false)}
      />
      <SendSms
        isOpen={smsModalOpen}
        msg={"Hi, "}
        phone={form?.phone || form?.user?.phone || form?.customer?.phone}
        onRequestClose={() => setSmsModalOpen(false)}
      />
      ;
    </div>
  );
};

export default DoctypeForm;
